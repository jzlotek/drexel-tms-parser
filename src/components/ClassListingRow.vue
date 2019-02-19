<template>
    <tr>
        <td class="text-xs-left">{{ props.item.course.title }}</td>
        <td>{{ props.item.semester }}</td>
        <td class="text-xs-left">
          {{ props.item.course.sc }} {{ props.item.course.cn }}-{{ props.item.sec }}
          </td>
        <td class="text-xs-left">{{ props.item.course.cr }}</td>
        <td class="text-xs-left">{{ props.item.instructor }}</td>
        <td class="text-xs-left">{{ props.item.course.it }}</td>
        <td class="text-xs-left">{{ props.item.course.im }}</td>
        <td class="text-xs-left">
          <span v-if="props.item.enrolled < props.item.maxEnroll">OPEN</span>
          <span v-else>FILLED</span>
        </td>
        <td class="text-xs-left">{{ props.item.enrolled }} / {{ props.item.maxEnroll }}</td>
        <td class="text-xs-left">
          <v-btn :href="props.item.crnLink" target="_blank">{{ props.item.crn }}</v-btn>
        </td>
        <td>
          <TimeDateDisplay
              :times="props.item.meeting">
          </TimeDateDisplay>
        </td>
        <td>
          <v-btn fab small @click="addToSelected()" color="secondary">
              <v-icon>add_circle</v-icon>
          </v-btn>
        </td>
    </tr>
</template>

<script>
import { ADD_TO_SELCTED } from '../store/constants';

/* webpackChunkName: "time-date-display" */
const TimeDateDisplay = () => import('./TimeDateDisplay');

export default {
  name: 'ClassListingRow',
  components: {
    TimeDateDisplay,
  },
  props: {
    props: {
      required: true,
    },
  },
  methods: {
    addToSelected() {
      this.$store.dispatch(ADD_TO_SELCTED, this.props.item);
    },
  },
};
</script>

<style>

</style>
