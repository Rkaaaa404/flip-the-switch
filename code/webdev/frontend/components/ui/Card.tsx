import React from "react";
import { cn } from "@/lib/utils";

type CardProps = React.ComponentProps<"div">;

export const Card = ({ className, children, ...props }: CardProps) => {
  return (
    <div 
      className={cn(
        "relative bg-white p-6 rounded-lg shadow-[0px_1px_2px_0px_rgba(0,0,0,0.05)] outline outline-1 outline-offset-[-1px] outline-slate-300/30 overflow-hidden", 
        className
      )} 
      {...props}
    >
      {children}
    </div>
  );
};
