import java.awt.BorderLayout;
import java.awt.Color;
import java.awt.Desktop;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.awt.image.BufferedImage;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.net.URI;
import java.net.URISyntaxException;
import java.util.Random;

import javax.imageio.ImageIO;
import javax.swing.JButton;
import javax.swing.JCheckBox;
import javax.swing.JComboBox;
import javax.swing.JFrame;
import javax.swing.JOptionPane;
import javax.swing.JPanel;
import javax.swing.Timer;
import org.openstreetmap.gui.jmapviewer.Coordinate;
import org.openstreetmap.gui.jmapviewer.JMapViewer;
import org.openstreetmap.gui.jmapviewer.MapMarkerDot;
import org.openstreetmap.gui.jmapviewer.MapPolygonImpl;
import org.openstreetmap.gui.jmapviewer.tilesources.OsmTileSource;

public class AnimationMapper extends JPanel implements ActionListener {
    private static final long serialVersionUID = 1L;
    private JComboBox<String> length;
	private JCheckBox include;
	private JButton start;
	private JCheckBox fun;
	private JMapViewer map;
	private Timer countDown;
	private int index;
	private IconMarker raccoon;
	private IconMarker sauce;
	private BufferedImage image;
	private BufferedImage image2;
	private MapMarkerDot path;
	private MapPolygonImpl trail;
	private URI rickRoll;
	private double maybe;
	private boolean done;
	

    public AnimationMapper() throws FileNotFoundException, IOException{
    	//Read in the file to establish all the ArrayLists.
    	TripPoint.readFile("triplog.csv");
    	
    	//Create the Frame to put the panel and map into
    	JFrame overview= new JFrame("Project 5 - Matthew Fitch");

		//Create the ComboBox to pick animation time
		String[] choices= {"Animation Time", "15", "30", "60", "90"};
		length=new JComboBox<>(choices);

		//Create the CheckBox to enable/disable stops
		include=new JCheckBox("Include Stops");

		//Extra Button for more fun
		fun=new JCheckBox("Icon");
		fun.addActionListener(this);

		//Create the Button
		start=new JButton("Play");
		start.addActionListener(this);

		//Add everything to the Panel
		JPanel inputs= new JPanel();
		inputs.setBounds(100,100,500,100);
		inputs.add(length);
		inputs.add(include);
		inputs.add(start);
		inputs.add(fun);
		
		//Create the MapViewer and establish the display position on open.
		map=new JMapViewer();
		map.setTileSource(new OsmTileSource.TransportMap());
		map.setDisplayPosition(new Coordinate(TripPoint.getTrip().get(100).getLat(), 
				TripPoint.getTrip().get(100).getLon()),6);
		
		//Make the raccoon head as the moving icon.
		File icon=new File("raccoon.png");
		image= ImageIO.read(icon);
		raccoon=new IconMarker(new Coordinate(TripPoint.getTrip().get(0).getLat(), 
				TripPoint.getTrip().get(0).getLon()), image);
		
		//Create a trail to highlight the path taken by the raccoon.
		path=new MapMarkerDot(Color.cyan,TripPoint.getTrip().get(0).getLat(), 
				TripPoint.getTrip().get(0).getLon());
		path.setBackColor(Color.cyan);
		path.setColor(Color.cyan);
		
		//Add the raccoon and the trail to the MapViewer
		map.addMapMarker(path);
		map.addMapMarker(raccoon);

		//Add the Panel and the map to the JFrame.
		overview.add(inputs, BorderLayout.NORTH);
		overview.add(map, BorderLayout.CENTER);
		
		//Establish the size of the JFrame on opening, and don't forget to make it visible.
		overview.setSize(1000, 1000);
		overview.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
		overview.setVisible(true);
		
		try {
			rickRoll=new URI("https://youtu.be/o-YBDTqX_ZU");
		} catch (URISyntaxException e) {
			JOptionPane.showMessageDialog(null, "Unable to roll at this time.", "ERROR", 
					JOptionPane.ERROR_MESSAGE);
			e.printStackTrace();
		}
		Random goodTimes= new Random();
		maybe=goodTimes.nextDouble();
		done=false;
    }
    
    public void actionPerformed(ActionEvent e) {
    	//Set a variable for if the CheckBox is selected or not.
    	boolean checked=this.include.isSelected();
    	boolean funTimes=this.fun.isSelected();
    	
    	//Establish what to do once the play button is pressed.
    	if(start==e.getSource()) {
        	
        	//Make sure to delete any previous animation first.
        	map.removeAllMapMarkers();
        	map.removeMapPolygon(trail);
    	
    		try {
    			//Read in the specific stop detection method desired to use.
				TripPoint.h1StopDetection();
			} catch (FileNotFoundException e1) {
				System.out.println("File not found.");
				e1.printStackTrace();
			} catch (IOException e1) {
				e1.printStackTrace();
			}
    		
    		//Establish what the value of time for animation is desired. Make
    		//a timer with that amount of time.
    		String length=String.valueOf(this.length.getSelectedItem());
        	int time = Integer.parseInt(length);
        	countDown=new Timer(time, this);
        	countDown.start();
        	index=0;
    	}
    	
    	//Once the timer starts, check to see if the CheckBox is checked or not.
    	else if(countDown.isRunning()) {
    		if(checked) {

    			//If checked, run through the trip ArrayList.
    			if(index<TripPoint.getTrip().size()-1) {

    				//Establish a trail for the path traveled.
//    				path.setBackColor(Color.cyan);
//    				path.setColor(Color.cyan);
    				

    				//Make sure to remove the raccoon head before adding the next one,
    				//to ensure the path is a paint trail and not a smudge of raccoon heads.
    				map.removeMapMarker(raccoon);

    				if(funTimes) {
    					if(maybe>.65 && !done) {
    						try {
    							Desktop.getDesktop().browse(rickRoll);
    							done=true;
    						}
    						catch (IOException e1) {
    							System.out.println("Sorry Charlie");
    							e1.printStackTrace();
    						}
    					}
    					else {
    						File options=new File("TartarSauce.png");
    						try {
    							image2=ImageIO.read(options);
    						} catch (IOException e1) {
    							System.out.println("No picture here");
    							e1.printStackTrace();
    						}
    					}
    					path.setBackColor(Color.cyan);
    					path.setColor(Color.cyan);
    					map.removeMapMarker(sauce);
    					map.removeMapMarker(raccoon);
    					path= new MapMarkerDot(Color.cyan, TripPoint.getTrip().get(index).getLat(), 
    							TripPoint.getTrip().get(index).getLon());
    					sauce=new IconMarker(new Coordinate(TripPoint.getTrip().get(index).getLat(),
    							TripPoint.getTrip().get(index).getLon()), image2);

    					//Ensure to add the trail in before the raccoon head to ensure priority for viewing.
    					map.addMapMarker(path);
    					map.addMapMarker(sauce);
    					index++;
    				}
    				else {
    					
    					Coordinate first=new Coordinate(TripPoint.getTrip().get(index).getLat(),
    							TripPoint.getTrip().get(index).getLon());
    					Coordinate second= new Coordinate(TripPoint.getTrip().get(index+1).getLat(),
    							TripPoint.getTrip().get(index+1).getLon());
    					trail=new MapPolygonImpl(first, second, second);
    					trail.setBackColor(Color.cyan);
    					trail.setColor(Color.cyan);
//    					path= new MapMarkerDot(Color.cyan, TripPoint.getTrip().get(index).getLat(), 
//    							TripPoint.getTrip().get(index).getLon());
    					raccoon=new IconMarker(new Coordinate(TripPoint.getTrip().get(index).getLat(),
    							TripPoint.getTrip().get(index).getLon()), image);

    					//Ensure to add the trail in before the raccoon head to ensure priority for viewing.
//    					map.addMapMarker(path);
    					map.addMapPolygon(trail);
    					map.addMapMarker(raccoon);
    					index++;
    				}
    			}
    		}
    		else if(!checked) {

    			//If the CheckBox is not checked then move through the MovingTrip ArrayList.
    			if(index<TripPoint.getMovingTrip().size()-1) {

    				if(funTimes) {
    					if(maybe>.65 && !done) {
    						try {
    							Desktop.getDesktop().browse(rickRoll);
    							done=true;
    						}
    						catch (IOException e1) {
    							System.out.println("Sorry Charlie");
    							e1.printStackTrace();
    						}
    					}
    					else {
    						File options=new File("TartarSauce.png");
    						try {
    							image2=ImageIO.read(options);
    						} catch (IOException e1) {
    							System.out.println("No picture here");
    							e1.printStackTrace();
    						}
    					}
    					path.setBackColor(Color.magenta);
    					path.setColor(Color.magenta);
    					map.removeMapMarker(sauce);
    					map.removeMapMarker(raccoon);
    					path= new MapMarkerDot(Color.magenta, 
    							TripPoint.getMovingTrip().get(index).getLat(),
    							TripPoint.getMovingTrip().get(index).getLon());
    					sauce=new IconMarker(new Coordinate(
    							TripPoint.getMovingTrip().get(index).getLat(),
    							TripPoint.getMovingTrip().get(index).getLon()), image2);

    					//Ensure to add the trail in before the raccoon head to ensure priority for viewing.
    					map.addMapMarker(path);
    					map.addMapMarker(sauce);
    					index++;
    				}
    				else {
    					//Establish the trail to highlight path taken.
//    					path.setBackColor(Color.magenta);
//    					path.setColor(Color.magenta);

    					//Remove raccoon to ensure just one raccoon head.
    					map.removeMapMarker(raccoon);
    					Coordinate first=new Coordinate(TripPoint.getMovingTrip().get(index).getLat(),
    							TripPoint.getMovingTrip().get(index).getLon());
    					Coordinate second= new Coordinate(TripPoint.getMovingTrip().get(index+1).getLat(),
    							TripPoint.getMovingTrip().get(index+1).getLon());
    					trail=new MapPolygonImpl(first, second, second);
    					trail.setBackColor(Color.magenta);
    					trail.setColor(Color.magenta);
//    					path= new MapMarkerDot(Color.magenta,
//    							TripPoint.getMovingTrip().get(index).getLat(), 
//    							TripPoint.getMovingTrip().get(index).getLon());
    					raccoon=new IconMarker(new Coordinate(
    							TripPoint.getMovingTrip().get(index).getLat(),
    							TripPoint.getMovingTrip().get(index).getLon()), image);

    					//Again establish the raccoon as what is in the foreground.
//    					map.addMapMarker(path);
    					map.addMapPolygon(trail);
    					map.addMapMarker(raccoon);
    					index++;
    				}
    			}
    		}
    	}
    }
}