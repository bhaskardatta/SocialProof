import { Card, CardHeader, CardTitle, CardDescription } from './Card';

function AppIcon({ icon: Icon, title, description, onClick, comingSoon = false }) {
  return (
    <Card
      onClick={!comingSoon ? onClick : undefined}
      className={`group transition-all duration-300 hover:scale-105 hover:shadow-2xl hover:shadow-primary-500/20 ${
        comingSoon ? 'opacity-60 cursor-not-allowed' : 'cursor-pointer'
      } relative overflow-hidden`}
    >
      {/* Hover gradient effect */}
      <div className="absolute inset-0 bg-gradient-to-br from-primary-600/0 via-primary-500/0 to-primary-600/0 group-hover:from-primary-600/10 group-hover:via-primary-500/5 group-hover:to-primary-600/10 transition-all duration-500"></div>
      
      <CardHeader className="relative">
        <div className="flex items-start justify-between">
          <div className="flex-1">
            <div className="mb-4 relative">
              <div className="h-16 w-16 rounded-2xl bg-gradient-to-br from-primary-500 to-primary-700 flex items-center justify-center group-hover:from-primary-400 group-hover:to-primary-600 transition-all duration-300 shadow-lg shadow-primary-500/30">
                {Icon && <Icon className="h-8 w-8 text-white" />}
              </div>
              {comingSoon && (
                <div className="absolute -top-2 -right-2 bg-yellow-500 text-gray-900 text-xs font-bold px-2 py-1 rounded-full">
                  Soon
                </div>
              )}
            </div>
            <CardTitle className="text-xl mb-2 group-hover:text-primary-400 transition-colors">
              {title}
            </CardTitle>
            <CardDescription className="text-gray-400 group-hover:text-gray-300 transition-colors">
              {description}
            </CardDescription>
          </div>
        </div>
      </CardHeader>
    </Card>
  );
}

export default AppIcon;
