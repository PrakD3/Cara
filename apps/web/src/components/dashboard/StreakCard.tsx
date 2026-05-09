import { Flame, Trophy } from "lucide-react";
import { Card } from "@/components/ui";

interface StreakCardProps {
	streak: number;
	xp: number;
	level: number;
}

export function StreakCard({ streak, xp, level }: StreakCardProps) {
	return (
		<Card className="p-6">
			<div className="flex items-center justify-between">
				<div className="flex items-center gap-4">
					<div className="w-12 h-12 bg-orange-100 rounded-2xl flex items-center justify-center">
						<Flame className="w-6 h-6 text-orange-500 fill-orange-500" />
					</div>
					<div>
						<p className="text-sm text-gray-500 font-medium uppercase tracking-wider">
							Current Streak
						</p>
						<p className="text-2xl font-bold text-gray-900">{streak} Days</p>
					</div>
				</div>
				<div className="text-right">
					<p className="text-sm text-gray-500 font-medium uppercase tracking-wider">
						Level {level}
					</p>
					<div className="flex items-center gap-1 text-indigo-600">
						<Trophy className="w-4 h-4" />
						<span className="font-bold">{xp} XP</span>
					</div>
				</div>
			</div>
			<div className="mt-4 w-full bg-gray-100 h-2 rounded-full overflow-hidden">
				<div
					className="bg-indigo-600 h-full rounded-full transition-all duration-500"
					style={{ width: `${xp % 100}%` }}
				/>
			</div>
		</Card>
	);
}
