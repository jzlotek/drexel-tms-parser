<template>
    <v-chip>{{ timeInner }}</v-chip>
</template>

<script>
import { get } from 'lodash';

export default {
  name: 'TimeDateChip',
  props: {
    time: {
      type: Object,
      required: true,
    },
  },
  computed: {
    timeInner() {
      return `${get(this.time, 'key')}: ${this.toString(get(this.time, 'value.start'))} to ${this.toString(get(this.time, 'value.end'))}`;
    },
  },
  methods: {
    toString(time) {
      let min = time % 60;
      let hour = Math.floor(time / 60);
      let ampm = 'AM';
      if (hour >= 12) {
        ampm = 'PM';
        if (hour > 12) {
          hour %= 12;
        } else if (hour === 24) {
          hour = 12;
          ampm = 'AM';
        }
      }
      if (min < 10) {
        min = `0${min}`;
      }
      return `${hour}:${min} ${ampm}`;
    },
  },
};
</script>

<style>

</style>
