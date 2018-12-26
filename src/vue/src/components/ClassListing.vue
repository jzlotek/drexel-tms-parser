<template>
  <div class="hello">
    <table v-if="hasClasses">
      <tr v-for="(c, index) in classes" :key="index">
        <td>{{ c.sc }}</td>
        <td>{{ c.cn }}</td>
        <td>{{ c.in }}</td>
        <td>{{ c.im }}</td>
        <td>{{ c.title }}</td>
        <td v-if="c.enrolled < c.maxEnroll">{{ c.enrolled }} / {{ c.maxEnroll }}</td>
        <td v-else>FILLED</td>
      </tr>
    </table>
    <p v-else>No classes found</p>
  </div>
</template>

<script>
export default {
  name: 'ClassListing',
  data() {
    return {
      // classes: [{ sc: 'MATH', cn: '101', enrolled: 10, maxEnroll: 50 }, { sc: 'CS', cn: '164' }],
      classes: [],
    };
  },
  computed: {
    hasClasses() {
      return this.classes.length > 0;
    },
  },
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
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
