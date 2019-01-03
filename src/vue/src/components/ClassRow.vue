<template>
    <tr>
        <td
          v-if="row && field.value !== 'enrolled'"
          v-for="(field, index) in fields"
          :key="index"
          class="text-xs-right">
            {{ row[field.value] }}
        </td>
        <td
          v-else-if="
            row
            && field.value === 'enrolled'
            && row['maxEnroll'] !== undefined
            && row['enrolled'] !== undefined
            && row['maxEnroll'] > row['enrolled']"
        >
            {{ row.maxEnroll - row.enrolled }} / {{ row.maxEnroll }} Open
        </td>
        <td
          class="text-xs-right"
          v-else-if="
            row
            && field.value === 'enrolled'"
        >
            FILLED
        </td>
        <td class="text-xs-right" v-else>
            {{ field.name }}
        </td>
    </tr>
</template>

<script>
export default {
  name: 'ClassRow',
  props: {
    row: {
      type: Object,
    },
    fields: {
      type: Array,
      required: true,
    },
  },
};
</script>

<style scoped>

</style>
