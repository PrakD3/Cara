"use client";

import { cn } from "@/components/ui";

type DosiState = "happy" | "neutral" | "sad" | "celebrating" | "sleeping";

interface DosiMascotProps {
	state: DosiState;
	className?: string;
}

export function DosiMascot({ state, className }: DosiMascotProps) {
	const stateEmojis: Record<DosiState, string> = {
		happy: "😊",
		neutral: "😐",
		sad: "😟",
		celebrating: "🎉",
		sleeping: "😴",
	};

	return (
		<div
			className={cn(
				"relative flex items-center justify-center w-32 h-32 bg-indigo-50 rounded-full border-4 border-indigo-200 animate-bounce",
				className,
			)}
		>
			<span className="text-6xl">{stateEmojis[state]}</span>
			<div className="absolute -bottom-2 px-3 py-1 bg-indigo-600 text-white text-xs font-bold rounded-full shadow-lg">
				DOSI
			</div>
		</div>
	);
}
