import { type ClassValue, clsx } from "clsx";
import { twMerge } from "tailwind-merge";

export function cn(...inputs: ClassValue[]) {
	return twMerge(clsx(inputs));
}

export function Card({
	className,
	children,
}: {
	className?: string;
	children: React.ReactNode;
}) {
	return (
		<div
			className={cn(
				"bg-white rounded-2xl shadow-sm border border-gray-100 overflow-hidden",
				className,
			)}
		>
			{children}
		</div>
	);
}

export function Button({
	className,
	variant = "primary",
	children,
	...props
}: React.ButtonHTMLAttributes<HTMLButtonElement> & {
	variant?: "primary" | "secondary" | "outline" | "ghost";
}) {
	const variants = {
		primary: "bg-indigo-600 text-white hover:bg-indigo-700",
		secondary: "bg-amber-500 text-white hover:bg-amber-600",
		outline: "border border-gray-200 text-gray-700 hover:bg-gray-50",
		ghost: "text-gray-600 hover:bg-gray-100",
	};

	return (
		<button
			className={cn(
				"px-4 py-2 rounded-xl font-medium transition-all active:scale-95 disabled:opacity-50 disabled:pointer-events-none",
				variants[variant],
				className,
			)}
			{...props}
		>
			{children}
		</button>
	);
}
