import { cn } from '../lib/utils';

export function Button({ className, variant = 'default', size = 'default', ...props }) {
  const baseStyles = 'inline-flex items-center justify-center rounded-lg text-sm font-medium transition-all focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50';
  
  const variants = {
    default: 'bg-primary-600 text-white hover:bg-primary-700 focus-visible:ring-primary-500',
    secondary: 'bg-gray-800 text-white hover:bg-gray-700 focus-visible:ring-gray-500',
    outline: 'border border-gray-700 bg-transparent hover:bg-gray-800 text-white',
    ghost: 'hover:bg-gray-800 text-white',
    danger: 'bg-danger-600 text-white hover:bg-danger-700 focus-visible:ring-danger-500',
    success: 'bg-success-600 text-white hover:bg-success-700 focus-visible:ring-success-500',
  };
  
  const sizes = {
    default: 'h-10 px-4 py-2',
    sm: 'h-9 px-3',
    lg: 'h-11 px-8',
    icon: 'h-10 w-10',
  };
  
  return (
    <button
      className={cn(baseStyles, variants[variant], sizes[size], className)}
      {...props}
    />
  );
}
