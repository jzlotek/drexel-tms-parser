<template>
  <div>
    <v-data-table
      :headers="headers"
      :items="items"
      :loading="isLoading"
      class="elevation-1"
    >
      <v-progress-linear slot="progress" color="red" indeterminate/>
      <template slot="no-data">
        <v-alert v-if="loadedOnce" :value="true" color="error">
          Sorry, no classes found :(
        </v-alert>
      </template>
      <template slot="items" slot-scope="props">
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
            <v-btn :href="props.item.crnLink">{{ props.item.crn }}</v-btn>
          </td>
          <td>
            <v-btn fab small @click="addToSelected(props.index)">
              <v-icon>add_circle</v-icon>
            </v-btn>
          </td>
        </tr>
      </template>
    </v-data-table>
    <v-btn @click="loadListing()">Reload</v-btn>
    <v-expansion-panel>
      <v-expansion-panel-content
        v-for="(item, index) in selected"
        :key="index"
      >
        <div slot="header">
          <v-btn fab small @click="removeFromSelected(index)">
            <v-icon>remove_circle</v-icon>
          </v-btn>
          {{ item.course.title }}
        </div>
        <v-card>
          <p class="text-xs-left">{{ item.course.title }}</p><br/>
          <p class="text-xs-center">{{ item.course.sc }}</p><br/>
          <p class="text-xs-center">{{ item.course.cn }}</p><br/>
          <p class="text-xs-center">{{ item.sec }}</p><br/>
          <p class="text-xs-center">{{ item.course.cr }}</p><br/>
          <p class="text-xs-center">{{ item.instructor }}</p><br/>
          <p class="text-xs-center">{{ item.course.it }}</p><br/>
          <p class="text-xs-center">{{ item.course.im }}</p>
        </v-card>
      </v-expansion-panel-content>
    </v-expansion-panel>
  </div>
</template>

<script>
import axios from 'axios';
import EventBus from '../EventBus';

export default {
  name: 'ClassListing',
  data() {
    return {
      isLoading: false,
      loadedOnce: false,
      items: [],
      selected: [],
      headers: [
        { text: 'Title', value: 'title', align: 'left' },
        { text: 'Subject Code', value: 'sc', align: 'center' },
        { text: 'Course Number', value: 'cn', align: 'center' },
        { text: 'Section', value: 'sec', align: 'center' },
        { text: 'Credits', value: 'cr', align: 'center' },
        { text: 'Instructor', value: 'instructor', align: 'center' },
        { text: 'Instruction Type', value: 'it', align: 'center' },
        { text: 'Instruction Method', value: 'im', align: 'center' },
        { text: 'Status', value: 'status', align: 'center' },
        { text: 'Enrolled', value: 'enrolled', align: 'center' },
        { text: 'CRN', value: 'crn', align: 'center' },
        { text: 'Add', value: '', align: 'center' },
      ],
    };
  },
  methods: {
    async loadListing() {
      this.isLoading = true;
      try {
        const response = await axios.get('/course?subject=CIVC');
        this.items = response.data;
      } catch (e) {
        EventBus.$emit('error', e);
      }
      this.isLoading = false;
      if (!this.loadedOnce) {
        this.loadedOnce = true;
      }
    },
    addToSelected(index) {
      this.selected.push(this.items[index]);
    },
    removeFromSelected(index) {
      this.selected.splice(index, 1);
    },
  },
};
</script>

<style>

</style>
