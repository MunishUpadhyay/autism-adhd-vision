import React, { useState, useRef, useEffect } from 'react';
import { analyzeVideo } from '../services/api';
import { Camera, Upload, Video, StopCircle, RefreshCw } from 'lucide-react';

const VideoInput = ({ onAnalysisStart, onAnalysisComplete, onAnalysisError }) => {
  const [inputMode, setInputMode] = useState('upload'); 
  const [videoSrc, setVideoSrc] = useState(null);
  
  const [isRecording, setIsRecording] = useState(false);
  const [recordingTime, setRecordingTime] = useState(0);
  const [hasRecorded, setHasRecorded] = useState(false);
  const [isProcessing, setIsProcessing] = useState(false);
  const [recordedVideoUrl, setRecordedVideoUrl] = useState(null);
  
  const MAX_RECORD_TIME = 6;
  
  const videoRef = useRef(null);
  const previewRef = useRef(null);
  const mediaRecorderRef = useRef(null);
  const chunksRef = useRef([]);
  const timerRef = useRef(null);
  
  const [stream, setStream] = useState(null);
  const [cameraError, setCameraError] = useState(null);

  const stopWebcam = () => {
    if (timerRef.current) clearInterval(timerRef.current);
    if (mediaRecorderRef.current && mediaRecorderRef.current.state !== 'inactive') {
      mediaRecorderRef.current.stop();
    }
    if (stream) {
      stream.getTracks().forEach(track => track.stop());
      setStream(null);
    }
  };

  // STEP 5: CLEAN OLD URL (PREVENT MEMORY BUG)
  const cleanupVideoUrl = () => {
    if (recordedVideoUrl) {
      URL.revokeObjectURL(recordedVideoUrl);
      setRecordedVideoUrl(null);
    }
  };

  useEffect(() => {
    if (inputMode === 'upload') {
      stopWebcam();
      cleanupVideoUrl();
    }
    return () => {
      stopWebcam();
      cleanupVideoUrl();
    };
  }, [inputMode]);

  const startWebcam = async () => {
    setCameraError(null);
    setVideoSrc(null);
    setIsRecording(false);
    setIsProcessing(false);
    cleanupVideoUrl();
    chunksRef.current = [];
    
    try {
      const mediaStream = await navigator.mediaDevices.getUserMedia({ video: true, audio: false });
      setStream(mediaStream);
      if (videoRef.current) {
        videoRef.current.srcObject = mediaStream;
      }
    } catch (err) {
      setCameraError("Camera access denied. Please allow permissions.");
    }
  };

  const handleUpload = async (file) => {
    if (!file) return;
    const url = URL.createObjectURL(file);
    setVideoSrc(url);
    onAnalysisStart();
    try {
      const result = await analyzeVideo(file);
      onAnalysisComplete(result);
    } catch (err) {
      onAnalysisError(err.message || "Failed to analyze media stream.");
    }
  };

  const startRecording = () => {
    if (!stream) return;
    chunksRef.current = [];
    setRecordingTime(0);
    setIsProcessing(false);
    cleanupVideoUrl(); // STEP 5
    
    // STEP 4: FIX MIME TYPE (VERY IMPORTANT)
    try {
      mediaRecorderRef.current = new MediaRecorder(stream, { mimeType: 'video/webm;codecs=vp8' });
    } catch (e) {
      mediaRecorderRef.current = new MediaRecorder(stream);
    }
    
    mediaRecorderRef.current.ondataavailable = (e) => {
      if (e.data && e.data.size > 0) {
        chunksRef.current.push(e.data);
      }
    };
    
    mediaRecorderRef.current.onstop = async () => {
      clearInterval(timerRef.current);
      setIsRecording(false);
      setRecordingTime(0);
      setIsProcessing(true); 
      
      // STEP 2: ENSURE URL IS CREATED PROPERLY
      const blob = new Blob(chunksRef.current, { type: "video/webm" });
      console.log("Blob size:", blob.size); // Logging explicitly 
      
      const file = new File([blob], "recorded.webm", { type: "video/webm" });
      const url = URL.createObjectURL(blob);
      setRecordedVideoUrl(url); 
      
      stopWebcam();
      
      onAnalysisStart();
      try {
        const result = await analyzeVideo(file);
        setIsProcessing(false); 
        
        if (result.motor_activity < 0.05 && result.movement_variance < 0.05) {
            onAnalysisError("Low visibility or insufficient motion detected. Please record again in better lighting.");
        } else {
            onAnalysisComplete(result);
        }
      } catch (err) {
        setIsProcessing(false);
        onAnalysisError(err.message || "Failed to parse continuous temporal recording.");
      }
    };
    
    mediaRecorderRef.current.start(500); 
    setIsRecording(true);
    
    timerRef.current = setInterval(() => {
      setRecordingTime((prev) => {
        if (prev >= MAX_RECORD_TIME - 1) {
          stopRecording(); 
          return prev + 1; 
        }
        return prev + 1;
      });
    }, 1000);
  };

  const stopRecording = () => {
    if (mediaRecorderRef.current && mediaRecorderRef.current.state !== 'inactive') {
      mediaRecorderRef.current.stop();
    }
  };

  // STEP 3: FORCE VIDEO LOAD + PLAY
  useEffect(() => {
    if (previewRef.current && recordedVideoUrl) {
        previewRef.current.load();
        previewRef.current.play().catch(() => {});
    }
  }, [recordedVideoUrl]);

  return (
    <div className="max-w-3xl mx-auto flex flex-col gap-4">
      <div className="flex bg-slate-200 p-1 rounded-full w-fit mx-auto shadow-inner">
        <button 
          onClick={() => setInputMode('upload')}
          disabled={isProcessing}
          className={`flex items-center gap-2 px-6 py-2 rounded-full font-bold text-sm transition-all ${inputMode === 'upload' ? 'bg-white text-indigo-600 shadow-sm' : 'text-slate-500 hover:text-slate-700'} ${isProcessing ? 'opacity-50 cursor-not-allowed' : ''}`}
        >
          <Upload className="w-4 h-4" /> Upload Video
        </button>
        <button 
          onClick={() => { setInputMode('webcam'); startWebcam(); }}
          disabled={isProcessing}
          className={`flex items-center gap-2 px-6 py-2 rounded-full font-bold text-sm transition-all ${inputMode === 'webcam' ? 'bg-white text-indigo-600 shadow-sm' : 'text-slate-500 hover:text-slate-700'} ${isProcessing ? 'opacity-50 cursor-not-allowed' : ''}`}
        >
          <Camera className="w-4 h-4" /> Use Webcam
        </button>
      </div>

      <div className="bg-slate-900 rounded-2xl overflow-hidden shadow-xl flex items-center justify-center relative border border-slate-800 aspect-video transition-all duration-300 group">
        
        {inputMode === 'upload' && (
          <>
            {videoSrc && (
              <label className="absolute top-4 right-4 bg-black/60 hover:bg-black/80 text-white text-xs px-4 py-2 rounded-full cursor-pointer backdrop-blur-md transition-all shadow-md z-10 border border-white/20 opacity-0 group-hover:opacity-100 flex items-center gap-2 font-semibold">
                <Upload className="w-3 h-3" /> Upload New
                <input type="file" accept="video/mp4,video/webm" className="hidden" onChange={(e) => handleUpload(e.target.files[0])} />
              </label>
            )}

            {videoSrc ? (
              <video src={videoSrc} controls className="w-full h-full object-contain bg-black" autoPlay muted />
            ) : (
              <div className="flex flex-col items-center justify-center text-slate-300 p-8 text-center max-w-sm animate-fade-in">
                <Video className="w-14 h-14 mb-4 opacity-40 text-indigo-400" />
                <h2 className="text-xl font-semibold mb-1 text-white">Upload Subject Media</h2>
                <p className="text-sm text-gray-400 mb-6 font-medium">Select a clinical video feed to begin dynamic tracking simulations</p>
                <label className="cursor-pointer bg-indigo-600 hover:bg-indigo-500 text-white hover:scale-105 px-8 py-3 rounded-full font-bold shadow-md transition-all duration-200">
                  Select Video File
                  <input type="file" accept="video/mp4,video/webm" className="hidden" onChange={(e) => handleUpload(e.target.files[0])} />
                </label>
              </div>
            )}
          </>
        )}

        {inputMode === 'webcam' && (
          <div className="w-full h-full flex flex-col items-center justify-center relative bg-black animate-fade-in">
            {cameraError ? (
              <div className="text-rose-500 font-bold px-6 py-4 bg-rose-500/10 rounded-xl border border-rose-500/20 text-center">
                <Camera className="w-8 h-8 mx-auto mb-2 opacity-50" />
                {cameraError}
              </div>
            ) : (
              <>
                {!recordedVideoUrl && (
                  <div className="absolute top-4 left-4 z-10 bg-black/50 px-4 py-1.5 rounded-full text-white/90 text-sm font-semibold backdrop-blur-sm border border-white/10 pointer-events-none flex items-center gap-2 shadow-sm">
                    <div className={`w-2.5 h-2.5 rounded-full ${isRecording ? 'bg-rose-500 animate-pulse' : 'bg-slate-400'}`}></div>
                    {isRecording ? 'Live Recording' : 'Live Preview'}
                  </div>
                )}
                
                {recordedVideoUrl && (
                  <div className="absolute top-4 left-4 z-10 bg-indigo-500/80 px-4 py-1.5 rounded-full text-white text-sm font-semibold backdrop-blur-sm border border-white/10 pointer-events-none shadow-sm shadow-indigo-500/20">
                    Recorded Sequence
                  </div>
                )}

                {isProcessing && (
                  <div className="absolute inset-0 z-20 flex items-center justify-center bg-black/70 backdrop-blur-[2px] transition-opacity duration-300">
                    <span className="bg-indigo-600 text-white font-black px-8 py-4 rounded-full flex items-center gap-3 animate-pulse shadow-lg border border-white/10">
                      <RefreshCw className="w-5 h-5 animate-spin" />
                      Analyzing recorded behavior...
                    </span>
                  </div>
                )}

                {/* STEP 1: FORCE REACT RE-RENDER OVERLAY */}
                {recordedVideoUrl ? (
                  <div className="w-full h-full relative">
                    <video 
                      key={recordedVideoUrl} 
                      ref={previewRef}
                      src={recordedVideoUrl} 
                      autoPlay 
                      loop 
                      muted 
                      controls
                      className="w-full h-full object-contain bg-black rounded-xl" 
                    />
                    
                    {/* STEP 6: FALLBACK DEBUG */}
                    <a 
                      href={recordedVideoUrl} 
                      download="test.webm" 
                      className="absolute top-4 right-4 z-30 bg-teal-500/90 hover:bg-teal-400 text-white font-bold text-xs px-4 py-2 rounded-full cursor-pointer shadow-lg backdrop-blur border border-white/20"
                    >
                      Download Video (Debug)
                    </a>
                  </div>
                ) : (
                  <video 
                    ref={videoRef} 
                    autoPlay 
                    playsInline 
                    muted 
                    className="w-full h-full object-cover" 
                  />
                )}

                {(stream || recordedVideoUrl) && !isProcessing && (
                  <div className="absolute bottom-6 left-0 right-0 flex justify-center z-10 transition-transform hover:scale-105">
                    {recordedVideoUrl ? (
                      <button 
                        onClick={startWebcam}
                        className="bg-indigo-500 hover:bg-indigo-400 text-white font-black px-10 py-4 rounded-full backdrop-blur-md shadow-[0_0_25px_rgba(0,0,0,0.5)] border border-white/20 flex items-center gap-3 transition-colors duration-300"
                      >
                        <Camera className="w-5 h-5" />
                        Record Another Video
                      </button>
                    ) : isRecording ? (
                      <button 
                        onClick={stopRecording}
                        className="bg-rose-600 hover:bg-rose-500 text-white font-black px-10 py-4 rounded-full backdrop-blur-md shadow-[0_0_25px_rgba(225,29,72,0.4)] border border-white/20 flex items-center gap-3 transition-colors duration-300"
                      >
                        <StopCircle className="w-5 h-5 animate-pulse" />
                        Recording... {recordingTime}s / {MAX_RECORD_TIME}s
                      </button>
                    ) : (
                      <button 
                        onClick={startRecording}
                        className="bg-indigo-600 hover:bg-indigo-500 text-white font-black px-10 py-4 rounded-full backdrop-blur-md shadow-[0_0_25px_rgba(0,0,0,0.5)] border border-white/20 flex items-center gap-3 transition-colors duration-300"
                      >
                        <Camera className="w-5 h-5" />
                        Start Recording
                      </button>
                    )}
                  </div>
                )}
              </>
            )}
          </div>
        )}

      </div>
    </div>
  );
};

export default VideoInput;
