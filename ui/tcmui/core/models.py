"""
Core remote objects.

"""
from .api import RemoteObject, ListObject, fields
from ..static.fields import StaticData



# Fake Company ID constant
SYSTEM_WIDE = -22222



class Company(RemoteObject):
    address = fields.Field()
    city = fields.Field()
    country = StaticData("COUNTRY")
    name = fields.Field()
    phone = fields.Field()
    url = fields.Field()
    zip = fields.Field()


    def __unicode__(self):
        return self.name



class CompanyList(ListObject):
    entryclass = Company
    api_name = "companies"
    default_url = "companies"

    entries = fields.List(fields.Object(Company))



class CategoryValueInfo(RemoteObject):
    categoryName = fields.Field()
    categoryValue = fields.Field()

    api_name = "CategoryValueInfo"


    def __unicode__(self):
        return u"%s: %s" % (self.categoryName, self.categoryValue)



class CategoryValueInfoList(ListObject):
    entryclass = CategoryValueInfo
    array_name = "CategoryValueInfo"

    entries = fields.List(fields.Object(CategoryValueInfo))


    def to_dict(self, enumclass, default=0):
        """
        Interpret the ``categoryName`` from each ``CategoryValueInfo`` as an
        identifier from the given enum class, and return a dictionary
        containing a key for every name in the enum, with values from each
        categoryValue, or ``default`` if no ``CategoryValueInfo`` is present
        for that enum value.

        For instance, given this enum:

        class SampleEnum(flufl.enum.Enum):
            ONE = 1
            TWO = 2

        If ``x`` is a ``CategoryValueInfoList`` containing a single
        ``CategoryValueInfo`` with categoryName=1 and categoryValue=5, a call
        to ``x.to_dict(SampleEnum)`` would return ``{"ONE": 5, "TWO": 0}``.

        """
        base = dict([(ev.enumname, default) for ev in enumclass])
        data = dict(
            [(enumclass[cvi.categoryName].enumname, cvi.categoryValue)
             for cvi in self])
        base.update(data)
        return base
