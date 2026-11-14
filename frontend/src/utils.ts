/**
 * Converts tick index (where t=0 is 08:00 AM, 5 minutes per tick) into HH:MM clock string.
 */
export function tickToClock(tick: number): string {
  const totalMinutes = 480 + tick * 5; // 08:00 is 480 minutes from midnight
  const hours = Math.floor(totalMinutes / 60);
  const minutes = totalMinutes % 60;
  return `${hours.toString().padStart(2, '0')}:${minutes.toString().padStart(2, '0')}`;
}
