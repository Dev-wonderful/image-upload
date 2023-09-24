upload = document.querySelector('.upload')
file = document.querySelector('.file')

upload.addEventListener('click', function(event){
    event.preventDefault()
    let upload_file = file.files
    console.log(upload_file[0])
    
    const formData = new FormData();
    formData.append('image', upload_file[0])
    response = fetch('http://127.0.0.1:5000/upload', {
        method: 'POST',
        mode: 'cors',
        // credentials: "include",
        // headers: {
        //     "Content-Type": "application/json"
        // },
        body: formData,
    }).then((response) => {
        console.log(response.json())
    })
})

// file.addEventListener('change', function(){
//     all_files = file.files
//     console.log('all_files:', all_files)
//     file = all_files[0]
//     console.log('file:', file)
// })
new_images = document.querySelector('.new_images')
image = document.querySelector('.image')


