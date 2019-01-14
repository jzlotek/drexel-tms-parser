<template>
  <v-container grid-list-md fluid text-xs-center>
    <v-layout row wrap justify-center>
      <v-flex grow xs6 md3 v-for="(dropdown, index) in dropdowns" :key="index">
        <SearchDropdown
          :fieldSlug="dropdown.fieldSlug"
          :fieldName="dropdown.fieldName"
          :apiEndpoint="dropdown.apiEndpoint"
          :affectedFields="dropdown.affectedFields"
          :queryParam="dropdown.queryParam"
          :clearQuery="dropdown.clearQuery"
        />
      </v-flex>
    </v-layout>
  </v-container>
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
      dropdowns: [
        {
          fieldSlug: 'subjectCode',
          fieldName: 'Subject Code',
          apiEndpoint: '/api/subject-codes',
          affectedFields: ['courseNumber'],
          queryParam: 'sc',
          clearQuery: true,
        },
        {
          fieldSlug: 'courseNumber',
          fieldName: 'Course Number',
          apiEndpoint: '/api/course-number',
          affectedFields: [''],
          queryParam: 'cn',
          clearQuery: false,
        },
        {
          fieldSlug: 'quarter',
          fieldName: 'Quarter',
          apiEndpoint: '/api/semester',
          affectedFields: ['subjectCode', 'courseNumber', 'colleges'],
          queryParam: 'semester',
          clearQuery: false,
        },
      ],
    };
  },
};
</script>
