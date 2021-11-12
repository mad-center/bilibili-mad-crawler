db.getCollection("mad").aggregate([
        {
            $project: {
                pubdate_str: {
                    $toDate: {
                        $multiply: [
                            "$pubdate",
                            1000
                        ]
                    }
                }
            }
        },
        {
            $match: {
                pubdate_str: {
                    $gte: ISODate("2009-01-01T00:00:00.000Z"),
                    $lt: ISODate("2010-01-01T00:00:00.000Z"),
                }
            }
        },
        {
            $sort: {
                pubdate_str: 1
            }
        }
    ],
    {
        allowDiskUse: true
    }
)