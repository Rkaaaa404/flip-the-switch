import { Loader2 } from "lucide-react";
import { cn } from "@/lib/utils";

type LoadingSpinnerProps = React.ComponentProps<"div"> & {
  iconClassName?: string;
};

export function LoadingSpinner({
  className,
  iconClassName,
  ...props
}: LoadingSpinnerProps) {
  return (
    <div
      className={cn(
        "absolute inset-0 z-50 flex items-center justify-center bg-black/40 backdrop-blur-sm",
        className
      )}
      {...props}
    >
      <Loader2
        role="status"
        aria-label="Loading"
        className={cn("size-8 animate-spin text-white", iconClassName)}
      />
    </div>
  );
}
