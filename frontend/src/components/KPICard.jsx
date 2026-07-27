import { motion } from 'framer-motion'
import { TrendingUp, TrendingDown, Minus } from 'lucide-react'

const trendIcons = {
  up: TrendingUp,
  down: TrendingDown,
  flat: Minus
}

export default function KPICard({ title, value, unit, trend, trend_direction = 'flat', color = '#7C3AED', index = 0 }) {
  const TrendIcon = trendIcons[trend_direction] || Minus

  return (
    <motion.div
      className="kpi-card"
      style={{ '--card-color': color }}
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.4, delay: index * 0.08 }}
      whileHover={{ y: -3 }}
    >
      <div className="kpi-title">{title}</div>
      <div className="kpi-value">
        {value}
        {unit && <span className="kpi-unit">{unit}</span>}
      </div>
      {trend !== undefined && trend !== null && (
        <div className={`kpi-trend ${trend_direction}`}>
          <TrendIcon size={12} />
          <span>{Math.abs(trend)}% vs last period</span>
        </div>
      )}
    </motion.div>
  )
}
