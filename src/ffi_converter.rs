use image::{DynamicImage, ImageReader};
use safer_ffi::prelude::*;
use std::io;
use std::path::PathBuf;

use crate::converter::{
    convert_image::{convert_iconset, convert_image, create_iconset},
    convert_struct::OutputFormat,
};

#[ffi_export]
pub fn ffi_create_iconset(input_path: char_p::Ref<'_>, output_dir_path: char_p::Ref<'_>) -> i32 {
    let input = PathBuf::from(input_path.to_str());
    let output = PathBuf::from(output_dir_path.to_str());

    let img: DynamicImage = match ImageReader::open(&input)
        .map_err(|e| io::Error::new(io::ErrorKind::Other, e.to_string()))
        .and_then(|reader| {
            reader
                .decode()
                .map_err(|e| io::Error::new(io::ErrorKind::InvalidData, e.to_string()))
        }) {
        Ok(img) => img,
        Err(_) => return 1,
    };

    match create_iconset(&[img], &output) {
        Ok(_) => 0,
        Err(_) => 2,
    }
}

#[ffi_export]
pub fn ffi_convert_iconset(
    folder_path: char_p::Ref<'_>,
    output_path: char_p::Ref<'_>,
    format: u32,
) -> i32 {
    let folder = PathBuf::from(folder_path.to_str());
    let output = PathBuf::from(output_path.to_str());

    let fmt = match format {
        0 => OutputFormat::Ico,
        1 => OutputFormat::Icns,
        _ => return 1,
    };

    match convert_iconset(&folder, &output, fmt) {
        Ok(_) => 0,
        Err(_) => 2,
    }
}

#[ffi_export]
pub fn ffi_convert_image(
    input_path: char_p::Ref<'_>,
    output_path: char_p::Ref<'_>,
    format: u32,
) -> i32 {
    let input = PathBuf::from(input_path.to_str());
    let output = PathBuf::from(output_path.to_str());

    let fmt = match format {
        0 => OutputFormat::Ico,
        1 => OutputFormat::Icns,
        _ => return 1,
    };

    let img = match ImageReader::open(&input)
        .map_err(|e| std::io::Error::new(std::io::ErrorKind::Other, e.to_string()))
        .and_then(|r| {
            r.decode()
                .map_err(|e| std::io::Error::new(std::io::ErrorKind::InvalidData, e.to_string()))
        }) {
        Ok(i) => i,
        Err(_) => return 2,
    };

    match convert_image(&img, &output, fmt) {
        Ok(_) => 0,
        Err(_) => 3,
    }
}
