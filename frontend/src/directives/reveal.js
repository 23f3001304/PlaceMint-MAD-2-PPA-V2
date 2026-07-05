// v-reveal: fades/slides an element in the first time it scrolls into view.
// Library-free scroll animation via IntersectionObserver.
const supported = typeof IntersectionObserver !== 'undefined'

const observer = supported
  ? new IntersectionObserver(
      (entries) => {
        for (const entry of entries) {
          if (entry.isIntersecting) {
            entry.target.classList.add('is-revealed')
            observer.unobserve(entry.target)
          }
        }
      },
      { threshold: 0.12, rootMargin: '0px 0px -8% 0px' },
    )
  : null

export const reveal = {
  mounted(el, binding) {
    el.classList.add('reveal')
    if (binding.value?.delay) el.style.transitionDelay = binding.value.delay
    if (observer) observer.observe(el)
    else el.classList.add('is-revealed')
  },
  unmounted(el) {
    observer?.unobserve(el)
  },
}
