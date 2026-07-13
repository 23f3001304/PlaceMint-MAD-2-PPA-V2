// Deterministic brand-tile colour for a company's initials avatar (used when no
// logo is uploaded). Same name always maps to the same colour.
const PALETTE = ['#1f6b3a', '#2f5f7f', '#94371f', '#7a5a12', '#5b4b8a', '#1f6b5f', '#8a5a1f']

export function avatarTint(name) {
  let h = 0
  for (let i = 0; i < (name || '').length; i++) h = (h * 31 + name.charCodeAt(i)) >>> 0
  return PALETTE[h % PALETTE.length]
}
