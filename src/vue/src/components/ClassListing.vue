<template>
  <div>
    <table v-if="hasClasses">
      <ClassRow :fields="fields"/>
      <ClassRow v-for="(cl, index) in classes" :key="index" :row="cl" :fields="fields"/>
    </table>
    <p v-else>No classes found</p>
  </div>
</template>

<script>
import ClassRow from './ClassRow';

export default {
  name: 'ClassListing',
  components: {
    ClassRow,
  },
  data() {
    return {
      classes: [{ sc: 'MATH', cn: '101', enrolled: 10, maxEnroll: 50 }, { sc: 'CS', cn: '164' }],
      fields: [
        { name: 'Title', value: 'title' },
        { name: 'Subject Code', value: 'sc' },
        { name: 'Course Number', value: 'cn' },
        { name: 'Section', value: 'sec' },
        { name: 'Credits', value: 'cr' },
        { name: 'CRN', value: 'crn' },
        { name: 'Instructor', value: 'in' },
        { name: 'Instruction Type', value: 'it' },
        { name: 'Instruction Method', value: 'im' },
        { name: 'Enrolled', value: 'enrolled' },
      ],
    };
  },
  computed: {
    hasClasses() {
      return this.classes.length > 0;
    },
  },
};
</script>

<style scoped>
h1, h2 {
  font-weight: normal;
}
ul {
  list-style-type: none;
  padding: 0;
}
li {
  display: inline-block;
  margin: 0 10px;
}
a {
  color: #42b983;
}
</style>
