<template>
  <div class="c-time-date">
    <div v-if="isNotTBD(times)">
      <div v-for="item in concatDict(times)" :key="item">
        <v-chip>{{ item.key }}: {{ toString(get(item.value, 'start')) }} to {{ toString(get(item.value, 'end')) }}</v-chip>
      </div>
    </div>
    <v-chip v-else d-inline-flex>TBD</v-chip>
  </div>
</template>

<script>
import { get as _get, isEqual, findIndex } from 'lodash';

export default {
  name: 'TimeDateDisplay',
  props: {
    times: {
      type: Object,
      required: false,
    },
  },
  methods: {
    isNotTBD(time) {
      return _get(time, 'TBD') !== 'TBD';
    },
    get(item, string) {
      return _get(item, string);
    },
    concatDict(timeDict) {
      if (Object.entries(timeDict).length == 0) {
        return [];
      }
      const order = 'MTWRFS';
      let l = Object.entries(timeDict).map(entry => 
        {
          return {
            key: entry[0],
            value: entry[1],
          };
      });

      const retList = [];

      l.forEach(entry => {
        let valueMap = retList.map(a => a.value);
        const i = findIndex(retList, 
          {
            value: {
              start: entry.value.start,
              end: entry.value.end
            }
          });
        if (i >= 0) {
          retList[i].key += entry.key;
        } else {
          retList.push(entry);
        }
      })
      
      return retList;
    },
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
.c-time-date {
  display: inline-flex;
}
</style>
