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
        <ClassListingRow :props="props"/>
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
          {{ item.course.title }}&nbsp;
          <v-btn :href="item.crnLink" target="_blank">{{ item.crn }}</v-btn>
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
import EventBus from '../EventBus';
import { UPDATE_CLASSES } from '../store';
import ClassListingRow from './ClassListingRow';

export default {
  name: 'ClassListing',
  components: {
    ClassListingRow,
  },
  computed: {
    items() {
      return this.$store.getters.getClasses;
    },
  },
  data() {
    return {
      isLoading: false,
      loadedOnce: false,
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
        { text: 'Time and Day', value: 'time_day', align: 'center' },
        { text: 'Add', value: '', align: 'center' },
      ],
    };
  },
  methods: {
    async loadListing() {
      this.isLoading = true;
      await this.$store.dispatch(UPDATE_CLASSES);
      this.isLoading = false;
    },
    addToSelected(index) {
      const item = this.items[index];
      if (this.selected.indexOf(item) === -1) {
        this.selected.push(item);
        EventBus.$emit('insert-to-weekview', item);
      } else {
        EventBus.$emit('error', `${item.crn} is already in your selected`);
      }
    },
    removeFromSelected(index) {
      this.selected.splice(index, 1);
      EventBus.$emit('remove-from-selected', index);
    },
  },
  mounted() {
    EventBus.$on('refresh-field', () => {
      this.loadListing();
    });
    EventBus.$on('add-to-selected', (index) => {
      this.addToSelected(index);
    });
  },
};
</script>

<style>

</style>
