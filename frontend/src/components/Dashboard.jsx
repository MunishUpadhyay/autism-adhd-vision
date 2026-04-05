import React from 'react';
import ScoreCard from './ScoreCard';
import IndicatorCard from './IndicatorCard';
import { Activity, Eye, Brain, LineChart, Target, Focus, CheckCircle2 } from 'lucide-react';

const Dashboard = ({ data }) => {
  if (!data) return null;

  const getPatternColor = (pattern) => {
    switch(pattern?.toLowerCase()) {
      case 'stable': return 'text-green-500';
      case 'repetitive': return 'text-yellow-500';
      case 'erratic': return 'text-red-500';
      default: return 'text-gray-500';
    }
  };

  // Explicit Fallbacks converting physical variance variables accurately
  const moveVar = data.movement_variance || 0.0;
  const trackLoss = data.eye_tracking_loss_rate || 0.0;
  
  // Calculate specific normalized metrics
  const eyeContactScore = Math.max(1.0 - trackLoss, 0.0);
  const attentionScore = Math.max(1.0 - moveVar, 0.0);
  const engagementScore = (eyeContactScore + attentionScore) / 2;

  // Use raw movement_variance mapping explicitly into our Variability limit
  const baseMotor = data.motor_activity || 0;

  return (
    <div className="max-w-4xl mx-auto space-y-8 animate-fade-in mt-4">
      
      {/* SECTION A: SCORE CARDS & EXTRACTED SIGNALS (Divider Set) */}
      <div className="border-t border-slate-200 pt-6">
        <h2 className="text-sm font-semibold text-gray-500 uppercase tracking-wide pl-2 mb-6">Extracted Signals</h2>
        
        {/* Row 1 */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-6">
          <ScoreCard title="Motor Activity" value={baseMotor} color="bg-blue-500" Icon={Activity} />
          <ScoreCard title="Eye Contact" value={eyeContactScore} color="bg-cyan-500" Icon={Eye} delayClass="delay-100" />
          <ScoreCard title="Attention Stability" value={attentionScore} color="bg-indigo-500" Icon={Brain} delayClass="delay-200" />
        </div>

        {/* Row 2 (Derived Variables) */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <ScoreCard title="Movement Variability" value={moveVar} color="bg-rose-500" Icon={LineChart} delayClass="delay-100" />
          <ScoreCard title="Gaze Stability" value={eyeContactScore} color="bg-emerald-500" Icon={Target} delayClass="delay-200" />
          <ScoreCard title="Engagement Level" value={engagementScore} color="bg-violet-500" Icon={Focus} delayClass="delay-300" />
        </div>
      </div>

      {/* SECTION B: BEHAVIOR PATTERN */}
      <div className="border-t border-slate-200 pt-6">
        <div className="bg-white rounded-2xl shadow-md p-6 w-full flex flex-col items-center justify-center text-center animate-fade-in delay-200 opacity-0">
          <h3 className="text-sm font-semibold text-gray-500 mb-2 uppercase tracking-wide">Primary Physical Pattern</h3>
          <span className={`text-3xl font-extrabold capitalize ${getPatternColor(data.behavior_pattern)}`}>
            {data.behavior_pattern}
          </span>
        </div>
      </div>

      {/* SECTION C: INDICATORS */}
      <div className="border-t border-slate-200 pt-6">
        <h2 className="text-sm font-semibold text-gray-500 uppercase tracking-wide pl-2 mb-6">Clinical Analysis</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <IndicatorCard title="ADHD Indicator" status={data.adhd_indicators} />
          <IndicatorCard title="Autism Indicator" status={data.autism_indicators} />
        </div>
      </div>

      {/* SECTION D: ANALYSIS SUMMARY */}
      <div className="border-t border-slate-200 pt-6 animate-fade-in delay-300 opacity-0">
        <div className="bg-slate-50 rounded-2xl shadow-sm p-8 w-full border border-slate-200 flex flex-col sm:flex-row items-center sm:items-start gap-4 mb-6">
          <div className="bg-white p-3 rounded-full shadow-sm">
            <CheckCircle2 className="w-8 h-8 text-indigo-500" />
          </div>
          <div className="flex flex-col text-center sm:text-left">
            <h3 className="text-sm font-bold text-slate-700 mb-1 uppercase tracking-wide mt-1">Analysis Summary</h3>
            <p className="text-gray-600 leading-relaxed font-medium">
              {data.reason || "Behavioral metrics successfully extracted globally."}
            </p>
          </div>
        </div>
      </div>

    </div>
  );
};

export default Dashboard;
