// The two lines below suppress compiler warnings that would confuse a learner. They are not part of the exercise.
#:property Nullable=disable
#:property PublishAot=false

// The runtime needs this registration before it can decode Windows-1252.
System.Text.Encoding.RegisterProvider(System.Text.CodePagesEncodingProvider.Instance);
// TODO: read customers-windows-1252.csv from the folder named by TRAINING_DATA, decoding it as Windows-1252.
// Then print the one line described in the lesson.
