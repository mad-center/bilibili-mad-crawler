use bilibili;
db.mad.aggregate([
    {
        $group: {
            _id: '$aid',
            dups: {
                $push: "$_id",
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
    }],
    {
        allowDiskUse: true
    })
    .forEach(function (doc) {
        doc.dups.shift();
        db.mad.remove({ _id: { $in: doc.dups } })
    });
