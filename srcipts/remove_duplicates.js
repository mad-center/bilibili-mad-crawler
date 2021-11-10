const query = [
  {
    $group: {
      _id: {
        field: "$field",
      },
      dups: {
        $addToSet: "$_id",
      },
      count: {
        $sum: 1,
      },
    },
  },
  {
    $match: {
      count: {
      $gt: 1,
      },
    },
  },
];

const cursor = collection.aggregate(query).cursor({ batchSize: 10 }).exec();

cursor.eachAsync((doc, i) => {
  doc.dups.shift(); // First element skipped for deleting
  doc.dups.map(async (dupId) => {
    await collection.findByIdAndDelete({ _id: dupId });
  });
});