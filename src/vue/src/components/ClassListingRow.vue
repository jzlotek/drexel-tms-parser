<template>
    <tr>
        <td class="text-xs-left">{{ props.item.course.title }}</td>
        <td class="text-xs-center">{{ props.item.course.sc }}</td>
        <td class="text-xs-center">{{ props.item.course.cn }}</td>
        <td class="text-xs-center">{{ props.item.sec }}</td>
        <td class="text-xs-center">{{ props.item.course.cr }}</td>
        <td class="text-xs-center">{{ props.item.instructor }}</td>
        <td class="text-xs-center">{{ props.item.course.it }}</td>
        <td class="text-xs-center">{{ props.item.course.im }}</td>
        <td class="text-xs-center">
          <span v-if="props.item.enrolled < props.item.maxEnroll">OPEN</span>
          <span v-else>FILLED</span>
        </td>
        <td class="text-xs-center">{{ props.item.enrolled }} / {{ props.item.maxEnroll }}</td>
        <td class="text-xs-center">
          <v-btn :href="props.item.crnLink" target="_blank">{{ props.item.crn }}</v-btn>
        </td>
        <td>
          <TimeDateDisplay
              :days="props.item.meeting.days"
              :times="props.item.meeting.times">
          </TimeDateDisplay>
        </td>
        <td>
          <v-btn fab small @click="addToSelected()">
              <v-icon>add_circle</v-icon>
          </v-btn>
        </td>
    </tr>
</template>

<script>
import TimeDateDisplay from './TimeDateDisplay';
import EventBus from './../EventBus';

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
      EventBus.$emit('add-to-selected', this.props.index);
    },
  },
};
</script>

<style>

</style>
