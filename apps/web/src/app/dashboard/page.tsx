"use client";

import { CheckCircle2, Clock, Pill, Loader2 } from "lucide-react";
import { DosiMascot } from "@/components/dashboard/DosiMascot";
import { StreakCard } from "@/components/dashboard/StreakCard";
import { Button, Card } from "@/components/ui";
import { useQuery } from "@tanstack/react-query";
import { getPatientProfile, getMedications } from "@/lib/api";

export default function DashboardPage() {
  const { data: patient, isLoading: isPatientLoading } = useQuery({
    queryKey: ["patient"],
    queryFn: getPatientProfile,
  });

  const { data: medications, isLoading: isMedsLoading } = useQuery({
    queryKey: ["medications", patient?.id],
    queryFn: () => getMedications(patient?.id),
    enabled: !!patient?.id,
  });

  if (isPatientLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50">
        <Loader2 className="w-8 h-8 text-indigo-600 animate-spin" />
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 pb-20">
      <header className="bg-white px-6 py-8 border-b border-gray-100">
        <h1 className="text-2xl font-bold text-gray-900">
          Good Morning, {patient?.user?.name || "Patient"}!
        </h1>
        <p className="text-gray-500">You're doing great today.</p>
      </header>

      <main className="p-6 space-y-6 max-w-2xl mx-auto">
        <div className="flex justify-center">
          <DosiMascot state={patient?.current_streak > 0 ? "happy" : "neutral"} />
        </div>

        <StreakCard 
          streak={patient?.current_streak || 0} 
          xp={patient?.total_xp || 0} 
          level={patient?.dosi_level || 1} 
        />

        <section>
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-lg font-bold text-gray-900">
              Today's Schedule
            </h2>
            <span className="text-sm text-indigo-600 font-medium">
              View All
            </span>
          </div>

          <div className="space-y-3">
            {isMedsLoading ? (
               <div className="flex justify-center py-8">
                 <Loader2 className="w-6 h-6 text-gray-400 animate-spin" />
               </div>
            ) : medications?.length === 0 ? (
               <p className="text-center text-gray-500 py-8">No medications scheduled for today.</p>
            ) : (
              medications?.map((med: any) => (
                <Card
                  key={med.id}
                  className="p-4 flex items-center justify-between"
                >
                  <div className="flex items-center gap-4">
                    <div className="text-indigo-500">
                      <Pill className="w-6 h-6" style={{ color: med.color }} />
                    </div>
                    <div>
                      <h3 className="font-bold text-gray-900">{med.name_encrypted}</h3>
                      <div className="flex items-center gap-2 text-sm text-gray-500">
                        <Clock className="w-3 h-3" />
                        <span>
                          {med.dosage} {med.unit}
                        </span>
                      </div>
                    </div>
                  </div>
                  <Button variant="outline" className="text-sm py-1.5 px-3">
                    Mark Taken
                  </Button>
                </Card>
              ))
            )}
          </div>
        </section>

        <Card className="p-6 bg-indigo-600 text-white">
          <h3 className="font-bold text-lg mb-2">AI Health Insight</h3>
          <p className="text-indigo-100 text-sm">
            {patient?.risk_level === "STABLE" 
              ? "Your adherence is perfect! Dosi is very happy with your progress."
              : "Dosi noticed you've been a bit irregular. Let's try to get back on track!"}
          </p>
        </Card>
      </main>
    </div>
  );
}
