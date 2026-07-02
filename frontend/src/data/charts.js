// Chart.js helpers tuned to the app palette (forest greens + warm accents).
export const PALETTE = [
  '#1f6b3a', '#c98a1a', '#3a6f8f', '#b0432b', '#4ab26a', '#6b6357', '#7a5a12',
]

// Turn a { label: count } map into a single-dataset Chart.js data object.
export function toChartData(map, label = '') {
  const labels = Object.keys(map || {})
  return {
    labels,
    datasets: [
      {
        label,
        data: labels.map((k) => map[k]),
        backgroundColor: labels.map((_, i) => PALETTE[i % PALETTE.length]),
        borderRadius: 6,
      },
    ],
  }
}
