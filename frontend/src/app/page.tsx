"use client";

import { CopilotSidebar } from "@copilotkit/react-ui";
import { useCoAgent } from "@copilotkit/react-core";

// State types matching the agent's state.py
type OnboardingState = {
  current_step: string;
  completed: boolean;
  role_preference: string | null;
  trinity: string | null;
  years_experience: number | null;
  industries: string[];
  location: string | null;
  remote_preference: string | null;
  target_compensation: string | null;
  availability: string | null;
};

type AgentState = {
  user: {
    id: string | null;
    email: string | null;
    name: string | null;
    profile_complete: boolean;
  };
  onboarding: OnboardingState;
  page_context: {
    current_page: string;
    page_type: string | null;
    role_context: string | null;
  };
  active_agent: string | null;
};

const INITIAL_STATE: AgentState = {
  user: {
    id: null,
    email: null,
    name: null,
    profile_complete: false,
  },
  onboarding: {
    current_step: "intro",
    completed: false,
    role_preference: null,
    trinity: null,
    years_experience: null,
    industries: [],
    location: null,
    remote_preference: null,
    target_compensation: null,
    availability: null,
  },
  page_context: {
    current_page: "/",
    page_type: "home",
    role_context: null,
  },
  active_agent: null,
};

// Map step names to human-readable labels
const STEP_LABELS: Record<string, string> = {
  intro: "Welcome",
  role_preference: "Your Role",
  trinity: "Engagement Type",
  experience: "Experience",
  location: "Location",
  search_prefs: "Preferences",
  completed: "Complete",
};

export default function Home() {
  const { state } = useCoAgent<AgentState>({
    name: "fractional_quest",
    initialState: INITIAL_STATE,
  });

  const onboarding = state?.onboarding || INITIAL_STATE.onboarding;
  const currentStep = onboarding.current_step || "intro";

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900">
      {/* Header */}
      <header className="border-b border-slate-700/50 bg-slate-900/50 backdrop-blur-sm">
        <div className="max-w-7xl mx-auto px-6 py-4">
          <h1 className="text-2xl font-bold text-white">
            Fractional<span className="text-emerald-400">Quest</span>
          </h1>
          <p className="text-slate-400 text-sm">
            AI-powered career platform for fractional executives
          </p>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-6 py-12">
        {/* Progress Steps */}
        <div className="mb-12">
          <div className="flex items-center justify-between max-w-3xl mx-auto">
            {Object.entries(STEP_LABELS).map(([step, label], index) => {
              const stepKeys = Object.keys(STEP_LABELS);
              const currentIndex = stepKeys.indexOf(currentStep);
              const isActive = step === currentStep;
              const isComplete = index < currentIndex || onboarding.completed;

              return (
                <div key={step} className="flex items-center">
                  <div className="flex flex-col items-center">
                    <div
                      className={`w-10 h-10 rounded-full flex items-center justify-center text-sm font-medium transition-all ${
                        isComplete
                          ? "bg-emerald-500 text-white"
                          : isActive
                          ? "bg-emerald-500/20 text-emerald-400 ring-2 ring-emerald-500"
                          : "bg-slate-700 text-slate-400"
                      }`}
                    >
                      {isComplete ? "✓" : index + 1}
                    </div>
                    <span
                      className={`mt-2 text-xs ${
                        isActive ? "text-emerald-400" : "text-slate-500"
                      }`}
                    >
                      {label}
                    </span>
                  </div>
                  {index < Object.keys(STEP_LABELS).length - 1 && (
                    <div
                      className={`w-12 h-0.5 mx-2 ${
                        index < currentIndex
                          ? "bg-emerald-500"
                          : "bg-slate-700"
                      }`}
                    />
                  )}
                </div>
              );
            })}
          </div>
        </div>

        {/* Profile Card */}
        <div className="max-w-2xl mx-auto">
          <div className="bg-slate-800/50 rounded-2xl border border-slate-700/50 p-8">
            <h2 className="text-xl font-semibold text-white mb-6">
              Your Profile
            </h2>

            <div className="grid grid-cols-2 gap-6">
              <ProfileItem
                label="Role"
                value={onboarding.role_preference?.toUpperCase()}
              />
              <ProfileItem
                label="Engagement"
                value={onboarding.trinity}
              />
              <ProfileItem
                label="Experience"
                value={
                  onboarding.years_experience
                    ? `${onboarding.years_experience} years`
                    : null
                }
              />
              <ProfileItem
                label="Location"
                value={onboarding.location}
              />
              <ProfileItem
                label="Remote"
                value={onboarding.remote_preference}
              />
              <ProfileItem
                label="Availability"
                value={onboarding.availability?.replace("_", " ")}
              />
            </div>

            {onboarding.industries.length > 0 && (
              <div className="mt-6">
                <span className="text-slate-400 text-sm">Industries</span>
                <div className="flex flex-wrap gap-2 mt-2">
                  {onboarding.industries.map((industry) => (
                    <span
                      key={industry}
                      className="px-3 py-1 bg-emerald-500/10 text-emerald-400 rounded-full text-sm"
                    >
                      {industry}
                    </span>
                  ))}
                </div>
              </div>
            )}
          </div>

          {/* Instructions */}
          <div className="mt-8 text-center">
            <p className="text-slate-400">
              Chat with the AI assistant on the right to complete your profile
            </p>
            <p className="text-slate-500 text-sm mt-2">
              Try saying: &quot;I&apos;m looking for fractional CTO roles&quot;
            </p>
          </div>
        </div>
      </main>

      {/* CopilotKit Sidebar */}
      <CopilotSidebar
        labels={{
          title: "Career Assistant",
          initial: "Hi! I'm your career assistant. Let's build your profile so I can help you find the perfect fractional executive role. What type of role are you looking for?",
          placeholder: "Type your message...",
        }}
        defaultOpen={true}
      />
    </div>
  );
}

function ProfileItem({
  label,
  value,
}: {
  label: string;
  value: string | null | undefined;
}) {
  return (
    <div>
      <span className="text-slate-400 text-sm">{label}</span>
      <p className="text-white font-medium mt-1">
        {value || <span className="text-slate-600">Not set</span>}
      </p>
    </div>
  );
}
