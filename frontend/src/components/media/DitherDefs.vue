<template>
  <!-- Global SVG filter defs. Mounted once (in App.vue); referenced by
       DitherImage via filter: url(#ppa-duotone). Maps a photo's luminance onto
       a forest-green -> cream ramp and posterizes it into 6 bands, which reads
       as a screen-printed duotone once the dot overlay is added. -->
  <svg aria-hidden="true" style="position: absolute; width: 0; height: 0">
    <defs>
      <filter id="ppa-duotone" color-interpolation-filters="sRGB">
        <feColorMatrix
          type="matrix"
          values="0.33 0.33 0.33 0 0
                  0.33 0.33 0.33 0 0
                  0.33 0.33 0.33 0 0
                  0    0    0    1 0"
        />
        <feComponentTransfer>
          <feFuncR type="discrete" tableValues="0.078 0.114 0.20 0.40 0.66 0.957" />
          <feFuncG type="discrete" tableValues="0.278 0.34 0.44 0.60 0.78 0.941" />
          <feFuncB type="discrete" tableValues="0.157 0.20 0.29 0.44 0.62 0.902" />
        </feComponentTransfer>
      </filter>
    </defs>
  </svg>
</template>
