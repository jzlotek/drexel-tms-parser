<template>
    <div class="class"
      v-bind:style="{
                    'margin-top': ctop,
                    'height': cheight,
                    'background-color': `${color}88`
                    }"
      >
        {{ className }}
    </div>
</template>

<script>
export default {
  name: 'WeekViewClass',
  data() {
    return {
      heightUnit: '91% / 16',
    };
  },
  props: {
    className: {
      type: String,
      required: true,
    },
    timeStart: {
      type: Number,
      required: true,
    },
    duration: {
      type: Number,
      required: true,
    },
    color: {
      type: String,
      required: true,
    },
  },
  computed: {
    // TODO: btter calc for getting the height and top properties
    cheight() {
      // gets height with respect to duration
      return `calc(${this.heightUnit} * ${this.duration})`;
    },
    ctop() {
      // gets top offset with reqpect to parent
      return `calc(${this.heightUnit} * ${this.timeStart - 6})`;
    },
  },
};
</script>

<style lang="scss">
.class {
  position: fixed;
  box-sizing: border-box;
  background-color: #db3ddb88;
  width: calc((100vw - 178px) * 0.2);
  z-index: 100;
  border-radius: 10px;
}
</style>
