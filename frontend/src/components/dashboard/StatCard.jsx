import { Card, CardHeader, CardContent } from '../Card';
import { cn } from '../../lib/utils';

/**
 * StatCard - Reusable card component for displaying statistics
 * 
 * This component provides a visually appealing way to display individual
 * statistics with an icon, title, value, and optional unit.
 * 
 * @param {Component} icon - Lucide icon component
 * @param {String} title - Stat title/label
 * @param {Number|String} value - Stat value
 * @param {String} unit - Optional unit (e.g., '%', 'pts')
 * @param {String} description - Optional description text
 * @param {String} variant - Color variant (primary, success, danger, warning)
 */
const StatCard = ({ 
  icon: Icon, 
  title, 
  value, 
  unit = '', 
  description,
  variant = 'primary' 
}) => {
  
  const variantClasses = {
    primary: 'from-primary-500 to-primary-700 shadow-primary-500/30',
    success: 'from-success-500 to-success-700 shadow-success-500/30',
    danger: 'from-danger-500 to-danger-700 shadow-danger-500/30',
    warning: 'from-yellow-500 to-yellow-700 shadow-yellow-500/30',
  };
  
  return (
    <Card className="border-gray-800 hover:border-gray-700 transition-all hover:shadow-xl">
      <CardContent className="p-6">
        <div className="flex items-start justify-between mb-4">
          <div className={cn(
            "h-12 w-12 rounded-xl bg-gradient-to-br flex items-center justify-center shadow-lg",
            variantClasses[variant]
          )}>
            <Icon className="w-6 h-6 text-white" />
          </div>
        </div>
        
        <div className="space-y-1">
          <p className="text-sm text-gray-400 font-medium">{title}</p>
          <div className="flex items-baseline gap-1">
            <p className="text-3xl font-bold text-white">{value}</p>
            {unit && <span className="text-lg text-gray-400">{unit}</span>}
          </div>
          {description && (
            <p className="text-xs text-gray-500 mt-2">{description}</p>
          )}
        </div>
      </CardContent>
    </Card>
  );
};

export default StatCard;
