<template>
  <div>
    <v-data-table
      :headers="headers"
      :items="items"
      :dark="true"
      :loading="isLoading"
      class="elevation-1"
    >
      <v-progress-linear slot="progress" color="red" indeterminate/>
      <template slot="items" slot-scope="props">
        <tr>
          <td class="text-xs-left">{{ props.item.course.title }}</td>
          <td class="text-xs-right">{{ props.item.course.sc }}</td>
          <td class="text-xs-right">{{ props.item.course.cn }}</td>
          <td class="text-xs-right">{{ props.item.sec }}</td>
          <td class="text-xs-right">{{ props.item.course.cr }}</td>
          <td class="text-xs-right">{{ props.item.instructor }}</td>
          <td class="text-xs-right">{{ props.item.course.it }}</td>
          <td class="text-xs-right">{{ props.item.course.im }}</td>
          <td class="text-xs-right">
            <span v-if="props.item.enrolled < props.item.maxEnroll">
              OPEN {{ props.item.enrolled }} / {{ props.item.maxEnroll }}
            </span>
            <span v-else>
              FILLED / {{ props.item.maxEnroll }}
            </span>
          </td>
          <td>
            <v-btn :href="props.item.crnLink">{{ props.item.crn }}</v-btn>
          </td>
        </tr>
      </template>
    </v-data-table>
    <v-btn @click="loadListing()">Reload</v-btn>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'ClassListing',
  data() {
    return {
      isLoading: false,
      items: [],
      headers: [
        { text: 'Title', value: 'title' },
        { text: 'Subject Code', value: 'sc' },
        { text: 'Course Number', value: 'cn' },
        { text: 'Section', value: 'sec' },
        { text: 'Credits', value: 'cr' },
        { text: 'Instructor', value: 'instructor' },
        { text: 'Instruction Type', value: 'it' },
        { text: 'Instruction Method', value: 'im' },
        { text: 'Enrolled', value: 'enrolled' },
        { text: 'CRN', value: 'crn' },
      ],
    };
  },
  methods: {
    loadListing() {
      this.isLoading = true;
      axios.get('/course?subject=CIVC')
        .then((response) => { this.items = response.data; })
        .catch(() => {});
      this.isLoading = false;
    },
  },
};
</script>

<style>

</style>
