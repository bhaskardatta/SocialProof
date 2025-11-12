import { cn } from '../lib/utils';

export function Input({ className, type, ...props }) {
  return (
    <input
      type={type}
      className={cn(
        'flex h-10 w-full rounded-lg border border-gray-700 bg-gray-800/50 px-3 py-2 text-sm text-white placeholder:text-gray-500 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent disabled:cursor-not-allowed disabled:opacity-50 transition-all',
        className
      )}
      {...props}
    />
  );
}
