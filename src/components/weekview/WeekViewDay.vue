<template>
  <div class="day">
    <table class="day-table">
      <tr class="hour" v-for="(i, index) in times" :key="index">
        <td>{{ i }}</td>
      </tr>
    </table>
    <div class="fixed-container" v-for="(c, index) in classes" :key="index">
      <WeekViewClass
        v-if="c.meeting.days.includes(dotw)"
        :className="c.course.title"
        :timeStart="c.timeStart"
        :duration="c.duration"
        color="#333333"></WeekViewClass>
    </div>
  </div>
</template>

<script>
const WeekViewClass = () => import('./WeekViewClass');

export default {
  name: 'WeekViewDay',
  computed: {
    times() {
      const arr = [];
      for (let i = this.timeStart; i < this.timeEnd; i += 1) {
        arr.push(i);
      }
      return arr;
    },
  },
  components: {
    WeekViewClass,
  },
  props: {
    classes: {
      type: Array,
    },
    dotw: {
      type: String,
      required: true,
    },
    timeStart: {
      type: Number,
      default: 7,
    },
    timeEnd: {
      type: Number,
      default: 23,
    },
  },
};
</script>

<style lang="scss">
.day {
  // position: absolute;
  background-color: rosybrown;
  border-radius: 10px;
  outline: 1px solid black;
  width: 100%;
  height: 100%;

  &-table {
    width: 100%;
    height: 100%;
  }
}
.hour {
  width: 100%;
  outline: 1px solid darkgrey;
}
.fixed-container {
  position: relative;
}
</style>
