package imageprocessing;

import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.net.MalformedURLException;
import java.net.URL;
import java.net.URLConnection;
import javax.imageio.ImageIO;
import java.io.BufferedReader;
import java.io.File;
import java.io.FileWriter;
import java.awt.image.BufferedImage;

public class ReadImage {
	public static final String ImageFoldUrl = "file:///lustre/storeB/users/thomasn/webcams/cropped_resized/";
	public static final String ObservationData = "file:///lustre/storeB/users/thomasn/webcams/data.csv";
	public static final String trainDataFile = "/disk1/git/skyrec/skyrec/java/src/imageprocessing/trainData.txt";
	public static final String testDataFile = "/disk1/git/skyrec/skyrec/java/src/imageprocessing/testData.txt";
	public static final boolean appendTrainData = true;
	public static final double trainPercent=0.7;
	
	public static String readRGBFromImage(String urlString) {
		String rgbString = "";

		BufferedImage bi;
		try {
			bi = ImageIO.read(new URL(urlString));

			int[] pixel;

			for (int y = 0; y < bi.getHeight(); y++) {
				for (int x = 0; x < bi.getWidth(); x++) {
					pixel = bi.getRaster().getPixel(x, y, new int[3]);
					rgbString+=","+pixel[0]+","+pixel[1]+","+pixel[2];
					//System.out
					//		.println(pixel[0] + " - " + pixel[1] + " - " + pixel[2] + " - " + (bi.getWidth() * y + x));
				}
			}
		} catch (IOException e1) {
			// TODO Auto-generated catch block
			e1.printStackTrace();
		}

		return rgbString.substring(1);
	}

	public static void listFiles(String urlString) {
		try {
			URL url = new URL(urlString);
			URLConnection conn = url.openConnection();
			InputStream inputStream = conn.getInputStream();
			BufferedReader reader = new BufferedReader(new InputStreamReader(inputStream));

			String line = null;
			int i = 0;
			while ((line = reader.readLine()) != null) {
				i++;
				System.out.println(line);
			}
			System.out.println("total files" + i);
			inputStream.close();
		} catch (IOException ex) {
			ex.printStackTrace();
		}
	}

	public static void createTrainDataSet() {
		URL dataUrl;
		String dataSeparator=",";
		try {
			dataUrl = new URL(ObservationData);
			BufferedReader in = new BufferedReader(new InputStreamReader(dataUrl.openStream()));

			String inputLine;
			//skip the first line
			in.readLine();
			while ((inputLine = in.readLine()) != null) {
				String[] values=inputLine.split(dataSeparator);
				if (values.length!=6)
					continue;
				String imageName=values[0];
				String weatherSymbol=values[4];
				String dataRow=readRGBFromImage(ImageFoldUrl+imageName);
				String[] rgbs=dataRow.split(",");
				dataRow="";
				int i=1;
				for (int j=0;j<rgbs.length;j++) {
					dataRow+=" "+(i++)+":"+rgbs[j];
				}
				dataRow=weatherSymbol+" "+dataRow.substring(1);
				if (Math.random()<=trainPercent) {
					appendToFile(dataRow,trainDataFile);
				} else {
					appendToFile(dataRow,testDataFile);
				}
				//System.out.println(imageName+":"+dataRow);
			}
			in.close();
		} catch (MalformedURLException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}

	}

	public static void appendToFile(String text, String fileName){
		if (text.isEmpty())
			return;
		try {
			File file = new File(fileName);

			FileWriter fw = new FileWriter(file, appendTrainData);
			fw.write(text+"\r\n");
			fw.close();

		} catch (IOException iox) {
			iox.printStackTrace();
		}
	}
	
	public static void main(String[] args) {
		//readRGBFromImage("file:///lustre/storeB/users/thomasn/webcams/cropped_resized/20160422_120002.jpg");

		//listFiles("file:///lustre/storeB/users/thomasn/webcams/cropped_resized/");
		createTrainDataSet();
		System.out.println("Done!");
	}
}