from System.Windows import Application
from System.Windows.Shapes import Rectangle
from System.Windows.Media import CaptureSource, CaptureState, VideoBrush, CaptureDeviceConfiguration
from System.Collections.ObjectModel import ObservableCollection
from System.Windows.Media.Imaging import WriteableBitmap

_CaptureSource = None
_Images = ObservableCollection[WriteableBitmap]()

def CaptureButton_Click(sender, e):
  if _CaptureSource is not None and _CaptureSource.State != CaptureState.Started:
    _CaptureSource.Stop() # stop whatever device may be capturing

    # set the devices for the capture source
    _CaptureSource.VideoCaptureDevice = xaml.VideoSources.SelectedItem;
    _CaptureSource.AudioCaptureDevice = xaml.AudioSources.SelectedItem;

    # create the brush
    vidBrush = VideoBrush()
    vidBrush.SetSource(_CaptureSource)
    xaml.WebcamCapture.Fill = vidBrush # paint the brush on the rectangle

    # request user permission and display the capture
    if CaptureDeviceConfiguration.AllowedDeviceAccess or CaptureDeviceConfiguration.RequestDeviceAccess():
      _CaptureSource.Start()

def StopCapture_Click(sender, e):
  if _CaptureSource is not None:
    _CaptureSource.Stop()

def TakeSnapshot_Click(sender, e):
  if _CaptureSource is not None and _CaptureSource.State == CaptureState.Started:
    _CaptureSource.CaptureImageAsync();
  else:
    window.Alert("Camera must be stared first")

def OnCaptureImage(s, e):
  _Images.Add(e.Result)

xaml = Application.Current.RootVisual
xaml.CaptureButton.Click += CaptureButton_Click
xaml.StopCapture.Click += StopCapture_Click
xaml.TakeSnapshot.Click += TakeSnapshot_Click

# get list of audio sources
xaml.AudioSources.ItemsSource = CaptureDeviceConfiguration.GetAvailableAudioCaptureDevices()

# get list of the video sources
xaml.VideoSources.ItemsSource = CaptureDeviceConfiguration.GetAvailableVideoCaptureDevices()

# creating a new capture source
_CaptureSource = CaptureSource()
_CaptureSource.CaptureImageCompleted += OnCaptureImage

# bind snapshot images
xaml.Snapshots.ItemsSource = _Images
