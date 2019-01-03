<template>
    <div>
      <SearchDropdown
        fieldName="subjectCode"
        apiEndpoint="/api/subject-codes"
        :affectedFields="subjectCode"
      />
      <SearchDropdown
        fieldName="courseNumber"
        apiEndpoint="/api/course-number"
        :affectedFields="courseNumber"
      />
      <SearchDropdown
        fieldName="colleges"
        apiEndpoint="/api/colleges"
        :affectedFields="colleges"
       />
      <button @click="refreshChildren()">Refresh</button>
      <br/>
      <button @click="executeQuery()">Execute Query</button>
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
