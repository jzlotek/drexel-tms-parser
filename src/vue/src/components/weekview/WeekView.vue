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
import WeekViewDay from './WeekViewDay';
import EventBus from '../../EventBus';

export default {
  name: 'WeekView',
  components: {
    WeekViewDay,
  },
  props: {
    classesInput: {
      type: Array,
    },
  },
  data() {
    return {
      classes: [],
    };
  },
  mounted() {
    this.classesInput.forEach((c) => {
      this.addClassToList(c);
    });
    EventBus.$on('insert-to-weekview', (c) => {
      this.addClassToList(c);
    });
    EventBus.$on('remove-from-selected', (index) => {
      this.classes.splice(index, 1);
    });
  },
  methods: {
    addClassToList(cl) {
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
      this.classes.push(c);
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

