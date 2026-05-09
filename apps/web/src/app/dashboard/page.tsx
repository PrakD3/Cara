import { CheckCircle2, Clock, Pill } from "lucide-react";
import { DosiMascot } from "@/components/dashboard/DosiMascot";
import { StreakCard } from "@/components/dashboard/StreakCard";
import { Button, Card } from "@/components/ui";

export default function DashboardPage() {
	const schedule = [
		{
			id: 1,
			name: "Metformin",
			dosage: "500mg",
			time: "08:00",
			status: "taken",
			slot: "MORNING",
		},
		{
			id: 2,
			name: "Atorvastatin",
			dosage: "20mg",
			time: "20:00",
			status: "pending",
			slot: "NIGHT",
		},
	];

	return (
		<div className="min-h-screen bg-gray-50 pb-20">
			<header className="bg-white px-6 py-8 border-b border-gray-100">
				<h1 className="text-2xl font-bold text-gray-900">
					Good Morning, Lakshmi!
				</h1>
				<p className="text-gray-500">You're doing great today.</p>
			</header>

			<main className="p-6 space-y-6 max-w-2xl mx-auto">
				<div className="flex justify-center">
					<DosiMascot state="happy" />
				</div>

				<StreakCard streak={12} xp={450} level={4} />

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
						{schedule.map((med) => (
							<Card
								key={med.id}
								className="p-4 flex items-center justify-between"
							>
								<div className="flex items-center gap-4">
									<div
										className={
											med.status === "taken"
												? "text-green-500"
												: "text-indigo-500"
										}
									>
										<Pill className="w-6 h-6" />
									</div>
									<div>
										<h3 className="font-bold text-gray-900">{med.name}</h3>
										<div className="flex items-center gap-2 text-sm text-gray-500">
											<Clock className="w-3 h-3" />
											<span>
												{med.time} • {med.dosage}
											</span>
										</div>
									</div>
								</div>
								{med.status === "taken" ? (
									<CheckCircle2 className="w-6 h-6 text-green-500" />
								) : (
									<Button variant="outline" className="text-sm py-1.5 px-3">
										Mark Taken
									</Button>
								)}
							</Card>
						))}
					</div>
				</section>

				<Card className="p-6 bg-indigo-600 text-white">
					<h3 className="font-bold text-lg mb-2">AI Health Insight</h3>
					<p className="text-indigo-100 text-sm">
						Based on your patterns, you're 20% more likely to miss your night
						dose. Try setting a reminder 15 minutes earlier!
					</p>
				</Card>
			</main>
		</div>
	);
}
