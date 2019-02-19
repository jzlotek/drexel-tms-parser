<template>
  <div class="c-time-date">
    <div v-if="isNotTBD">
      <div v-for="item in timeList" :key="item">
        <TimeDateChip :time="item" />
      </div>
    </div>
    <v-chip v-else d-inline-flex>TBD</v-chip>
  </div>
</template>

<script>
import { get, findIndex } from 'lodash';
import TimeDateChip from './TimeDateChip.vue';

export default {
  name: 'TimeDateDisplay',
  components: {
    TimeDateChip,
  },
  props: {
    times: {
      type: Object,
      required: false,
    },
  },
  computed: {
    isNotTBD() {
      return get(this.times, 'TBD') !== 'TBD';
    },
    timeList() {
      if (Object.entries(this.times).length === 0) {
        return [];
      }
      const l = Object.entries(this.times).map(entry => ({
        key: entry[0],
        value: entry[1],
      }));

      const retList = [];

      l.forEach((entry) => {
        const i = findIndex(retList,
          {
            value: {
              start: entry.value.start,
              end: entry.value.end,
            },
          });
        if (i >= 0) {
          retList[i].key += entry.key;
        } else {
          retList.push(entry);
        }
      });

      return retList;
    },
  },
};
</script>

<style>
.c-time-date {
  display: inline-flex;
}
</style>
