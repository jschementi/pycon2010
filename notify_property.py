import clrtype
import pyevent
from System.ComponentModel import INotifyPropertyChanged, PropertyChangedEventArgs

class NotifyPropertyChangedBase(INotifyPropertyChanged):
    PropertyChanged = None

    def __init__(self):
        self.PropertyChanged, self._propertyChangedCaller = pyevent.make_event()

    def add_PropertyChanged(self, value):
        self.PropertyChanged += value

    def remove_PropertyChanged(self, value):
        self.PropertyChanged -= value

    def OnPropertyChanged(self, propertyName):
        if self.PropertyChanged is not None:
            self._propertyChangedCaller(self, PropertyChangedEventArgs(propertyName))

class notify_property(property):

    def __init__(self, getter):
        def newgetter(slf):
            #return None when the property does not exist yet
            try:
                return getter(slf)
            except AttributeError:
                return None
        getter = clrtype.accepts()(getter)
        clrtype.propagate_attributes(getter, newgetter)
        super(notify_property, self).__init__(newgetter)

    def setter(self, setter):
        def newsetter(slf, newvalue):
            # do not change value if the new value is the same
            # trigger PropertyChanged event when value changes
            oldvalue = self.fget(slf)
            if oldvalue != newvalue:
                setter(slf, newvalue)
                slf.OnPropertyChanged(setter.__name__)
        setter = clrtype.returns()(setter)
        clrtype.propagate_attributes(setter, newsetter)
        return property(
            fget=self.fget,
            fset=newsetter,
            fdel=self.fdel,
            doc=self.__doc__)
