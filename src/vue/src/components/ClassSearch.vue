<template>
    <div>
      <SearchDropdown
        fieldSlug="subjectCode"
        fieldName="Subject Code"
        apiEndpoint="/api/subject-codes"
        :affectedFields="subjectCode"
        queryParam="sc"
        :clearQuery="true"
      />
      <SearchDropdown
        fieldSlug="courseNumber"
        fieldName="Course Number"
        apiEndpoint="/api/course-number"
        :affectedFields="courseNumber"
        queryParam="cn"
      />
      <!-- <SearchDropdown
        fieldName="colleges"
        apiEndpoint="/api/colleges"
        :affectedFields="colleges"
       /> -->
    </div>
</template>
<script>
const SearchDropdown = () => import('./search/SearchDropdown');

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
};
</script>
