use super::convert_struct::OutputFormat;
use icns::{IconFamily, IconType, Image as IcnsImage};
use ico::{IconDir, IconImage};
use image::{DynamicImage, GenericImageView};
use std::{
    fs::{self, File},
    io::{self, BufReader, Result},
    path::Path,
};
use tempfile::TempDir;

fn convert_to_ico(pngs: &[std::fs::DirEntry], output: &Path) -> io::Result<()> {
    let mut icon_dir = IconDir::new(ico::ResourceType::Icon);

    for entry in pngs {
        let img = image::open(entry.path())
            .map_err(|e| io::Error::new(io::ErrorKind::InvalidData, e.to_string()))?;
        let (w, h) = img.dimensions();
        let rgba = img.to_rgba8();
        let icon_image = IconImage::from_rgba_data(w, h, rgba.into_raw());
        let entry = ico::IconDirEntry::encode(&icon_image)
            .map_err(|e| io::Error::new(io::ErrorKind::InvalidData, e.to_string()))?;
        icon_dir.add_entry(entry);
    }

    let writer = File::create(output)?;
    icon_dir.write(writer)?;
    Ok(())
}

pub fn convert_to_icns(pngs: &[std::fs::DirEntry], output: &Path) -> io::Result<()> {
    let mut icon_family = IconFamily::new();

    for entry in pngs {
        let file = File::open(entry.path())?;
        let reader = BufReader::new(file);
        let icns_img = IcnsImage::read_png(reader)
            .map_err(|e| io::Error::new(io::ErrorKind::InvalidData, e.to_string()))?;

        let w = icns_img.width();
        let h = icns_img.height();
        let icon_type = IconType::from_pixel_size(w, h)
            .ok_or(format!("Unsupported size: {}x{}", w, h))
            .map_err(|e| io::Error::new(io::ErrorKind::InvalidInput, e))?;
        icon_family.add_icon_with_type(&icns_img, icon_type)?;
    }
    let mut out = File::create(output)?;
    icon_family.write(&mut out)?;
    Ok(())
}

pub fn create_iconset(images: &[DynamicImage], output_dir: &Path) -> Result<()> {
    if !output_dir.exists() {
        fs::create_dir_all(output_dir)?;
    }
    let sizes = [16, 32, 64, 128, 256, 512];

    if images.len() != 1 {
        return Err(io::Error::new(
            io::ErrorKind::InvalidInput,
            "Expecting a single image",
        ));
    }

    let img = &images[0];
    let (orig_width, orig_height) = img.dimensions();

    for &size in sizes.iter() {
        let resized_img = img.resize(size, size, image::imageops::FilterType::Lanczos3);
        let output_path = output_dir.join(format!("icon_{}x{}.png", size, size));
        resized_img
            .save(&output_path)
            .map_err(|e| io::Error::new(io::ErrorKind::Other, e.to_string()))?;

        if orig_width >= size * 2 && orig_height >= size * 2 {
            let resized_2x_img =
                img.resize(size * 2, size * 2, image::imageops::FilterType::Lanczos3);
            let output_path_2x = output_dir.join(format!("icon_{}x{}@2x.png", size, size));
            resized_2x_img
                .save(&output_path_2x)
                .map_err(|e| io::Error::new(io::ErrorKind::Other, e.to_string()))?;
        }
    }

    Ok(())
}

pub fn convert_iconset(folder: &Path, output: &Path, format: OutputFormat) -> io::Result<()> {
    let pngs = fs::read_dir(folder)?
        .filter_map(Result::ok)
        .filter(|e| {
            e.path()
                .extension()
                .map(|ext| ext.eq_ignore_ascii_case("png"))
                .unwrap_or(false)
        })
        .collect::<Vec<_>>();

    if pngs.is_empty() {
        return Err(io::Error::new(
            io::ErrorKind::NotFound,
            "No PNG files found in the folder.",
        ));
    }

    match format {
        OutputFormat::Ico => convert_to_ico(&pngs, output),
        OutputFormat::Icns => convert_to_icns(&pngs, output),
    }
}

pub fn convert_image(
    input_image: &DynamicImage,
    output: &Path,
    format: OutputFormat,
) -> Result<()> {
    let temp_dir = TempDir::new()?;
    let iconset_folder = temp_dir.path().join("iconset");
    create_iconset(&[input_image.clone()], &iconset_folder)?;
    convert_iconset(&iconset_folder, output, format)?;
    Ok(())
}
