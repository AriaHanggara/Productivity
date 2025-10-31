- Saya menggunakan Odoo 19.0.
- Saya menggunakan method api.depends dibandingkan method override karena pada kasus ini hanya melakukan komputasi sederhana (juga karena sistem caching ORM Odoo), bila ada komputasi yang lebih kompleks seperti diperlukannya validasi sebelum data disimpan, lebih baik menggunakan method override,
  walaupun lebih kompleks (dan tidak adanya sistem caching), tetapi dapat memberi kontrol penuh pada alur eksekusi.
- Pada kasus konversi dari gram ke kilogram, pertama saya tidak menggunakan @api.depends(), berhasil dan lancar, besoknya saya buka lagi malah bug, fields yang lainnya masuk
  tetapi fields konversi tidak masuk. Setelah saya coba menggunakan @api.depends(), alhamdulillah lancar jaya sampai sekarang. Dan pada bagian upload ke Odoo Online dimana
  saya menggunakan fitur gratis, disana tidak bisa mengupload file .py sehingga harus membuat model dan komputasi manual. Beda jika menggunakan Odoo.sh atau hostingan lain, bisa langsung mengimport custom addons
  beserta file .py nya.
- Maap saya kurang mengerti bagian "performance considerations for large datasets".

Saya menyertakan productivity online dan offline dimana terdapat perbedaan penulisan variabel pada views .xml, untuk folder online, tinggal melakukan zip dan import pada Odoo Online, begitupun sebaliknya.

terimakasih, sehat selalu
