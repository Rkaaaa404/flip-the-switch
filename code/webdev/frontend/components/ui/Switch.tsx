"use client";

import { Switch as SwitchPrimitive } from "radix-ui";

type SwitchProps = {
  checked: boolean;
  onCheckedChange: (checked: boolean) => void;
  disabled?: boolean;
  id?: string;
};

export function Switch({
  checked,
  onCheckedChange,
  disabled,
  id,
}: SwitchProps) {
  return (
    <SwitchPrimitive.Root
      checked={checked}
      onCheckedChange={onCheckedChange}
      disabled={disabled}
      id={id || "airplane-mode"}
      className="peer inline-flex h-6 w-11 shrink-0 cursor-pointer items-center rounded-full border-2 border-transparent transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-orange-500 focus-visible:ring-offset-2 focus-visible:ring-offset-white disabled:cursor-not-allowed disabled:opacity-50 data-[state=checked]:bg-orange-500 data-[state=unchecked]:bg-gray-200"
    >
      <SwitchPrimitive.Thumb
        className="pointer-events-none block h-5 w-5 rounded-full bg-white shadow-sm ring-0 transition-transform duration-200 data-[state=checked]:translate-x-5 data-[state=unchecked]:translate-x-0"
      />
    </SwitchPrimitive.Root>
  );
}
