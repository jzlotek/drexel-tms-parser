<template>
    <div>
      <v-container grid-list-md fluid ext-xs-center>
        <v-layout row wrap justify-center>
          <v-flex grow xs6 md3>
            <SearchDropdown
              fieldSlug="subjectCode"
              fieldName="Subject Code"
              apiEndpoint="/api/subject-codes"
              :affectedFields="subjectCode"
              queryParam="sc"
              :clearQuery="true"
            />
          </v-flex>
          <v-flex grow xs6 md3>
            <SearchDropdown
              fieldSlug="courseNumber"
              fieldName="Course Number"
              apiEndpoint="/api/course-number"
              :affectedFields="courseNumber"
              queryParam="cn"
            />
          </v-flex>
          <v-flex grow xs6 md3>
            <SearchDropdown
              fieldSlug="year"
              fieldName="Year"
              apiEndpoint="/api/years"
              :affectedFields="year"
              queryParam="year"
              :def="getCurrentYear()"
            />
          </v-flex>
        </v-layout>
      </v-container>
    </div>
</template>
<script>
import axios from 'axios';

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
      year: ['subjectCode', 'courseNumber', 'colleges'],
    };
  },
  methods: {
    async getCurrentYear() {
      let year = await axios.get('/api/current-year');
      year = year.data;
      return year;
    }
  },
};
</script>
