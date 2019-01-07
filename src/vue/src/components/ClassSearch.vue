<template>
    <div>
      <SearchDropdown
        fieldName="subjectCode"
        apiEndpoint="/api/subject-codes"
        :affectedFields="subjectCode"
        queryParam="sc"
        :clearQuery="true"
      />
      <SearchDropdown
        fieldName="courseNumber"
        apiEndpoint="/api/course-number"
        :affectedFields="courseNumber"
        queryParam="cn"
      />
      <!-- <SearchDropdown
        fieldName="colleges"
        apiEndpoint="/api/colleges"
        :affectedFields="colleges"
       /> -->
      <v-btn color="primary" @click="refreshChildren()">Refresh</v-btn>
      <br/>
      <v-btn color="primary" @click="executeQuery()">Execute Query</v-btn>
    </div>
</template>
<script>
import SearchDropdown from './search/SearchDropdown';
import EventBus from '../EventBus';

export default {
  name: 'ClassSearch',
  components: {
    SearchDropdown,
  },
  data() {
    return {
      subjectCode: ['courseNumber'],
      courseNumber: [''],
      colleges: ['subjectCode', 'courseNumber'],
    };
  },
  methods: {
    refreshChildren() {
      EventBus.$emit('refresh-search');
    },
    executeQuery() {
      EventBus.$emit('execute-query');
    },
  },
};
</script>
