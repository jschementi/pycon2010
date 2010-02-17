from System.Windows import Application
Application.Current.LoadRootVisualFromString(open("app.xaml").read())
Application.Current.RootVisual.loading.Text = "Hello from Python!"
