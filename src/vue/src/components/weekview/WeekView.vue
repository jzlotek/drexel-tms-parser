<template>
    <div class="container">
      <WeekViewDay
        v-for="(day, index) in 'MTWRF'"
        :key="index"
        :classes="classes"
        :dotw="day">
      </WeekViewDay>
    </div>
</template>

<script>
/* webpackChunkName: "week-view-day */
const WeekViewDay = () => import('./WeekViewDay');

export default {
  name: 'WeekView',
  components: {
    WeekViewDay,
  },
  computed: {
    classes() {
      const cls = [];
      this.classesFromState.forEach((cl) => {
        const c = cl;
        if (c.meeting.times && c.meeting.times.length > 0) {
          const timeArrStart = c.meeting.times[0].split(':');
          const timeArrEnd = c.meeting.times[1].split(':');
          const timeStartUnitNumber = parseInt(timeArrStart[0], 10)
                + (parseInt(timeArrStart[1], 10) / 60);
          const timeStart = (parseInt(timeArrStart[0], 10) * 60)
                + parseInt(timeArrStart[1], 10);
          const timeEnd = (parseInt(timeArrEnd[0], 10) * 60)
                + parseInt(timeArrEnd[1], 10);
          const duration = (timeEnd - timeStart) / 60;
          c.timeStart = timeStartUnitNumber;
          c.duration = duration;
        }
        cls.push(c);
      });
      return cls;
    },
    classesFromState() {
      return this.$store.getters.getSelected;
    },
  },
};
</script>


<style lang="scss">
.container {
  height: 100%;
  width: 100%;
  display: flex;
  position: relative;
}
</style>

