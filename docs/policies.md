# Policies 
```
$ lenticular policies
```

Lenticular is set up to manage files for large projects. This assumes that you'll have hundreds or thousands of files  that need to be fetched from the cloud, processed and published as a dataset. 

The policies file allows you to set rules that can be applied to the entire collection. For example, what is the maxiumum file size? If you set `image.output_size` to 4Mb, then all image files will be resized to less than the limit. If you want all jpg or png files for the web, the policy rules will convert all formats to your preferred file types. 

To configure your project and define its policies, enter `$ lenticular policies` and follow the prompts.

With the policies saved, you can now download and  [normalize](../normalization) the files. 

More on file format and filename standards
- https://developer.mozilla.org/en-US/docs/Web/Media/Formats
- https://guides.library.upenn.edu/datamgmt/fileorg